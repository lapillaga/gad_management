import json

from docxtpl import DocxTemplate

import frappe
from frappe import _
from frappe.model.document import Document
from gad_management.common import get_template_url_from_settings, \
    get_docx_template_io, GENERATED_DOCX_PATH, generate_file_response, \
    get_gad_settings
from gad_management.gad_app_management.doctype.gad_member.selectors import \
    get_gad_member_doc
from gad_management.gad_app_management.doctype.gad_memo.selectors import \
    get_gad_memo_doc
from gad_management.gad_app_management.doctype.gad_memo_template.selectors import \
    get_gad_memo_template_doc
from gad_management.utils import get_formatted_date

SETTINGS_TEMPLATE_FIELD_NAME = "memo_template"


@frappe.whitelist()
def download_word(doc_name: str):
    """
    Generate a Word document based on a template or base template
    and download it
    """
    template_url = None
    document = get_gad_memo_doc(doc_name)

    if not document:
        frappe.throw(_('El Memo especificado no existe'))

    if document.template:
        template_document = get_gad_memo_template_doc(document.template)

        if template_document.template:
            template_url = template_document.template

    if not template_url:
        template_url = get_template_url_from_settings(
            SETTINGS_TEMPLATE_FIELD_NAME
        )

    template_io = get_docx_template_io(template_url)
    doc = DocxTemplate(template_io)
    settings_doc = get_gad_settings()
    sender_dict = get_gad_member_doc(document.sender).as_dict()
    recipient_dict = get_gad_member_doc(document.recipient).as_dict()

    doc.render({
        'memo_number': document.name,
        'subject': document.subject,
        'parish': settings_doc.get("parish") or 'Jerusalén',
        'document_date': get_formatted_date(document.date),
        'recipient': recipient_dict,
        'content': document.content,
        'sender': sender_dict,
        'attachments': document.attachments or [],
    })
    doc.save(GENERATED_DOCX_PATH)

    with open(GENERATED_DOCX_PATH, "rb") as output_file_obj:
        filedata = output_file_obj.read()

    generate_file_response(filedata, template_url)


class GadMemo(Document):
    pass
