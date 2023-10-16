from docxtpl import DocxTemplate, R

import frappe
from frappe.model.document import Document
from frappe import _
from gad_management.common import get_template_url_from_settings, \
    get_docx_template_io, get_gad_settings, GENERATED_DOCX_PATH, \
    generate_file_response
from gad_management.gad_app_management.doctype.gad_member.gad_member import \
    SECRETARY_TREASURER, PRESIDENT
from gad_management.gad_app_management.doctype.gad_member.selectors import \
    get_gad_member_by_role
from gad_management.gad_app_management.doctype.gad_payment_justification.selectors import \
    get_gad_payment_justification_doc
from gad_management.utils import get_formatted_date


@frappe.whitelist()
def download_word(doc_name: str, template_field_name: str):
    """
    Generate a Word document based on a template or base template
    and download it
    """
    template_url = get_template_url_from_settings(template_field_name)
    document = get_gad_payment_justification_doc(doc_name)

    if not document.parties:
        frappe.throw(_('Debe especificar al menos un beneficiario'))

    template_io = get_docx_template_io(template_url)
    doc = DocxTemplate(template_io)
    settings_doc = get_gad_settings()
    secretary_dict = get_gad_member_by_role(SECRETARY_TREASURER)
    president_dict = get_gad_member_by_role(PRESIDENT)
    parties = []
    for party in document.parties:
        parties.append(party.as_dict())

    doc.render({
        "parish": settings_doc.get("parish") or 'Jerusalén',
        "document_date": get_formatted_date(document.date),
        "budget": document.budget,
        "secretary": secretary_dict,
        "president": president_dict,
        "parties": document.parties,
        'page_break': R('\f'),
    })
    doc.save(GENERATED_DOCX_PATH)

    with open(GENERATED_DOCX_PATH, "rb") as output_file_obj:
        filedata = output_file_obj.read()
    generate_file_response(filedata, template_url)


class GadPaymentJustification(Document):
    pass
