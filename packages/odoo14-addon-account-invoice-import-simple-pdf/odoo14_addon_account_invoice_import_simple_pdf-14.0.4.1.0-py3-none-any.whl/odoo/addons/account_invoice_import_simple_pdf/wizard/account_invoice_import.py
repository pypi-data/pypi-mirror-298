# Copyright 2021 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
import shutil
import subprocess
from tempfile import NamedTemporaryFile

from odoo import _, api, models
from odoo.exceptions import UserError
from odoo.osv import expression

logger = logging.getLogger(__name__)
try:
    import fitz
except ImportError:
    logger.debug("Cannot import PyMuPDF")
try:
    import regex
except ImportError:
    logger.debug("Cannot import regex")
try:
    import pdftotext
except ImportError:
    logger.debug("Cannot import pdftotext")
try:
    import pypdf
except ImportError:
    logger.debug("Cannot import pypdf")


class AccountInvoiceImport(models.TransientModel):
    _inherit = "account.invoice.import"

    @api.model
    def fallback_parse_pdf_invoice(self, file_data):
        """This method must be inherited by additional modules with
        the same kind of logic as the account_bank_statement_import_*
        modules"""
        res = super().fallback_parse_pdf_invoice(file_data)
        if not res:
            res = self.simple_pdf_parse_invoice(file_data)
        return res

    @api.model
    def _simple_pdf_text_extraction_pymupdf(self, fileobj, test_info):
        res = False
        version = None
        try:
            pages = []
            doc = fitz.open(fileobj.name)
            for page in doc:
                pages.append(page.get_text())
            res = {
                "all": "\n\n".join(pages),
                "first": pages and pages[0] or "",
            }
            # For PyMuPDF, we used to get the version via __version__
            # but it is not possible with newer version of the lib
            if hasattr(fitz, "__version__"):
                version = fitz.__version__
            elif hasattr(fitz, "version") and isinstance(fitz.version, tuple):
                version = fitz.version[0]
            logger.info("Text extraction made with PyMuPDF %s", version)
            test_info["text_extraction"] = "pymupdf %s" % version
        except Exception as e:
            logger.warning("Text extraction with PyMuPDF failed. Error: %s", e)
        return res

    @api.model
    def _simple_pdf_text_extraction_pypdf(self, fileobj, test_info):
        res = False
        try:
            reader = pypdf.PdfReader(fileobj.name)
            pages = []
            for pdf_page in reader.pages:
                pages.append(pdf_page.extract_text())
                res = {
                    "all": "\n\n".join(pages),
                    "first": pages and pages[0] or "",
                }
            test_info["text_extraction"] = "pypdf %s" % pypdf.__version__
            logger.info("Text extraction made with pypdf %s", pypdf.__version__)
        except Exception as e:
            logger.warning("Text extraction with pypdf failed. Error: %s", e)
        return res

    @api.model
    def _simple_pdf_pdftotext_cmd_call(self, fileobj, test_info, first_page=False):
        res = False
        if not shutil.which("pdftotext"):
            logger.warning(
                "Could not find the pdftotext utility. Hint: sudo apt install poppler-utils"
            )
            return False
        cmd_args = ["pdftotext"]
        if first_page:
            cmd_args += ["-l", "1"]
        cmd_args += ["-layout", fileobj.name, "-"]
        try:
            out, err = subprocess.Popen(cmd_args, stdout=subprocess.PIPE).communicate()
            if err:
                logger.debug("pdftotext_cmd err=%s", err)
            if out:
                res = out.decode("utf8")
        except Exception as e:
            logger.info("Text extraction with pdftotext command failed. Error: %s", e)
        return res

    @api.model
    def _simple_pdf_text_extraction_pdftotext_cmd(self, fileobj, test_info):
        res_all = self._simple_pdf_pdftotext_cmd_call(fileobj, test_info)
        if not res_all:
            return False
        res = {
            "all": res_all,
            "first": self._simple_pdf_pdftotext_cmd_call(
                fileobj, test_info, first_page=True
            ),
        }
        test_info["text_extraction"] = "pdftotext.cmd"
        logger.info("Text extraction made with pdftotext command")
        return res

    @api.model
    def _simple_pdf_text_extraction_pdftotext_lib(self, fileobj, test_info):
        # pdftotext lib doc: https://github.com/jalan/pdftotext
        res = False
        try:
            with open(fileobj.name, "rb") as pdf_file:
                pdf = pdftotext.PDF(pdf_file)
                res = {
                    "all": "\n\n".join(pdf),
                    "first": pdf[0],
                }
            logger.info("Text extraction made with pdftotext lib")
            test_info["text_extraction"] = "pdftotext.lib"
        except Exception as e:
            logger.warning("Text extraction with pdftotext lib failed. Error: %s", e)
        return res

    @api.model
    def _simple_pdf_text_extraction_specific_tool(
        self, specific_tool, fileobj, test_info
    ):
        res = False
        if specific_tool == "pymupdf":
            res = self._simple_pdf_text_extraction_pymupdf(fileobj, test_info)
        elif specific_tool == "pdftotext.lib":
            res = self._simple_pdf_text_extraction_pdftotext_lib(fileobj, test_info)
        elif specific_tool == "pdftotext.cmd":
            res = self._simple_pdf_text_extraction_pdftotext_cmd(fileobj, test_info)
        elif specific_tool == "pypdf":
            res = self._simple_pdf_text_extraction_pypdf(fileobj, test_info)
        else:
            raise UserError(
                _(
                    "System Parameter 'invoice_import_simple_pdf.pdf2txt' "
                    "has an invalid value '%s'."
                )
                % specific_tool
            )
        if not res:
            raise UserError(
                _(
                    "Odoo could not extract the text from the PDF invoice "
                    "with the method %s. Refer to the Odoo server logs for more technical "
                    "information about the cause of the failure."
                )
                % specific_tool
            )
        return res

    @api.model
    def simple_pdf_text_extraction(self, file_data, test_info):
        specific_tool = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("invoice_import_simple_pdf.pdf2txt")
        )
        if specific_tool:
            specific_tool = specific_tool.strip().lower()
        test_info["text_extraction_config"] = specific_tool

        with NamedTemporaryFile(
            "wb", prefix="odoo-simple-pdf-", suffix=".pdf"
        ) as fileobj:
            fileobj.write(file_data)
            fileobj.seek(0)
            # Extract text from PDF
            # Very interesting reading:
            # https://dida.do/blog/how-to-extract-text-from-pdf
            # https://github.com/erfelipe/PDFtextExtraction
            if specific_tool:
                res = self._simple_pdf_text_extraction_specific_tool(
                    specific_tool, fileobj, test_info
                )
            else:
                # From best tool to worst
                res = self._simple_pdf_text_extraction_pymupdf(fileobj, test_info)
                if not res:
                    res = self._simple_pdf_text_extraction_pdftotext_lib(
                        fileobj, test_info
                    )
                if not res:
                    res = self._simple_pdf_text_extraction_pdftotext_cmd(
                        fileobj, test_info
                    )
                if not res:
                    res = self._simple_pdf_text_extraction_pypdf(fileobj, test_info)
                if not res:
                    raise UserError(
                        _(
                            "Odoo could not extract the text from the PDF invoice. "
                            "Refer to the Odoo server logs for more technical information "
                            "about the cause of the failure."
                        )
                    )
        for key, text in res.items():
            if text:
                # Remove lonely accents
                # example : Free mobile invoices for months with accents
                # i.e. février, août, décembre
                # that are extracted as f´evrier, aoˆut, d´ecembre
                res[key] = regex.sub(test_info["lonely_accents"], "", text)

        res["all_no_space"] = regex.sub(
            "%s+" % test_info["space_pattern"], "", res["all"]
        )
        res["first_no_space"] = regex.sub(
            "%s+" % test_info["space_pattern"], "", res["first"]
        )
        return res

    @api.model
    def _simple_pdf_keyword_fields(self):
        return {
            "vat": _("VAT number"),
        }

    @api.model
    def simple_pdf_match_partner(self, raw_text_no_space, test_results=None):
        if test_results is None:
            test_results = []
        partner_id = False
        rpo = self.env["res.partner"]
        # Warning: invoices have the VAT number of the supplier, but they often
        # also have the VAT number of the customer (i.e. the VAT number of our company)
        # So we exclude it from the search
        keyword_fields_dict = self._simple_pdf_keyword_fields()
        keyword_fields_list = list(keyword_fields_dict.keys())
        domain_or_list = [[(field, "!=", False)] for field in keyword_fields_list]
        domain_or_list.append([("simple_pdf_keyword", "!=", False)])
        field_domain = expression.OR(domain_or_list)
        partners = rpo.search_read(
            field_domain
            + [
                ("parent_id", "=", False),
                ("is_company", "=", True),
                ("id", "!=", self.env.company.partner_id.id),
            ],
            ["simple_pdf_keyword"] + keyword_fields_list,
        )
        for partner in partners:
            if partner["simple_pdf_keyword"] and partner["simple_pdf_keyword"].strip():
                keywords = partner["simple_pdf_keyword"].replace(" ", "").split("|")
                found_res = [keyword in raw_text_no_space for keyword in keywords]
                if all(found_res):
                    partner_id = partner["id"]
                    result_label = _("Successful match on %d keywords (%s)") % (
                        len(keywords),
                        ", ".join(keywords),
                    )
                    test_results.append("<li>%s</li>" % result_label)
                    break
            for kfield, kfield_label in keyword_fields_dict.items():
                if partner[kfield] and partner[kfield] in raw_text_no_space:
                    partner_id = partner["id"]
                    result_label = _("Successful match on {label} '{value}'").format(
                        label=kfield_label,
                        value=partner[kfield],
                    )
                    test_results.append("<li>%s</li>" % result_label)
                    break
        return partner_id

    @api.model
    def _get_space_pattern(self):
        # https://en.wikipedia.org/wiki/Whitespace_character
        # I cannot use \p{White_space} because it includes carriage return
        space_ints = [
            32,
            160,
            8192,
            8193,
            8194,
            8195,
            8196,
            8197,
            8198,
            8199,
            8200,
            8201,
            8202,
            8239,
            8287,
        ]
        return "[%s]" % "".join([chr(x) for x in space_ints])

    @api.model
    def _get_lonely_accents(self):
        lonely_accents = [
            "\u00B4",  # acute accent
            "\u0060",  # grave accent
            "\u005E",  # circumflex accent
            "\u00A8",  # diaeresis
            "\u02CA",  # modifier letter acute accent
            "\u02CB",  # modifier letter grave accent
            "\u02C6",  # modifier letter circumflex accent
        ]
        return "[%s]" % "".join(lonely_accents)

    @api.model
    def _simple_pdf_update_test_info(self, test_info):
        aiispfo = self.env["account.invoice.import.simple.pdf.fields"]
        test_info.update(
            {
                "date_format_sel": dict(
                    aiispfo.fields_get("date_format", "selection")["date_format"][
                        "selection"
                    ]
                ),
                "field_name_sel": dict(
                    aiispfo.fields_get("name", "selection")["name"]["selection"]
                ),
                "extract_rule_sel": dict(
                    aiispfo.fields_get("extract_rule", "selection")["extract_rule"][
                        "selection"
                    ]
                ),
                "space_pattern": self._get_space_pattern(),
                "lonely_accents": self._get_lonely_accents(),
            }
        )

    @api.model
    def simple_pdf_parse_invoice(self, file_data, test_info=None):
        if test_info is None:
            test_info = {"test_mode": False}
        self._simple_pdf_update_test_info(test_info)
        rpo = self.env["res.partner"]
        logger.info("Trying to analyze PDF invoice with simple pdf module")
        raw_text_dict = self.simple_pdf_text_extraction(file_data, test_info)
        partner_id = self.simple_pdf_match_partner(raw_text_dict["all_no_space"])
        if not partner_id:
            parsed_inv = {"chatter_msg": ["Simple PDF Import: count not find Vendor."]}
            return parsed_inv
        partner = rpo.browse(partner_id)
        raw_text = (
            partner.simple_pdf_pages == "first"
            and raw_text_dict["first"]
            or raw_text_dict["all"]
        )
        logger.info(
            "Simple pdf import found partner %s ID %d", partner.display_name, partner_id
        )
        partner_config = partner._simple_pdf_partner_config()
        parsed_inv = {
            "partner": {"recordset": partner},
            "currency": {"recordset": partner_config["currency"]},
            "failed_fields": [],
            "chatter_msg": [],
        }

        # Check field config
        for field in partner.simple_pdf_field_ids:
            logger.debug("Working on field %s", field.name)
            try:
                getattr(field, "_get_%s" % field.name)(
                    parsed_inv, raw_text, partner_config, test_info
                )
            except AttributeError:
                raise UserError(
                    _("Missing parse method for field '%s'. This should never happen.")
                    % field.name
                )

        failed_fields = parsed_inv.pop("failed_fields")
        if failed_fields:
            parsed_inv["chatter_msg"].append(
                _("<b>Failed</b> to extract the following field(s): %s.")
                % ", ".join(
                    [
                        "<b>%s</b>" % test_info["field_name_sel"][failed_field]
                        for failed_field in failed_fields
                    ]
                )
            )

        logger.info("simple pdf parsed_inv=%s", parsed_inv)
        return parsed_inv
