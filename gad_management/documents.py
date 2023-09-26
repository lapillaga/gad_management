import json
import os
from io import BytesIO

import requests
from docxtpl import DocxTemplate

import frappe
from frappe import _
from frappe.utils import get_files_path
from gad_management.utils import get_formatted_date
from werkzeug.wrappers import Response

DOCUMENT_CONTEXT_MAPPING = {
    'po_template_1': lambda document: get_doc_1_context(document),
}
GENERATED_DOCX_PATH = '/tmp/generated.docx'
GENERATED_PDF_PATH = '/tmp/generated.pdf'
PSPDF_KIT_API_KEY = "pdf_live_tTlugWcsAsarYv6yA5UFJzUgtueXXqiXVpv8SNJmaWW"


def get_doc_1_context(document):
    """
    Generate the context for the doc_1 document.
    Doc_1 belongs to 1. Certificado de disponibilidad de bienes
    """
    settings_doc = get_gad_settings()
    responsible = frappe.get_doc(
        "Gad Member",
        document.doc_1_responsible,
    )
    available_stock = document.available_stock
    return {
        'parish': settings_doc.get("parish") or 'Jerusalén',
        'document_date': get_formatted_date(document.document_date),
        'role_name': responsible.role_name or '',
        'responsible_name': responsible.full_name,
        'responsible_title': responsible.title,
        'existing_materials': available_stock,
        'gad_name': settings_doc.get("gad_name") or 'GAD Jerusalén',
    }


def get_gad_purchase_doc(doc_name: str):
    """
    Get the GAD purchase order Document
    """
    gad_purchase_doc = frappe.get_doc(
        "Gad Purchase Document",
        doc_name,
    )

    if not gad_purchase_doc:
        frappe.throw(_('Por favor debe crear una Documento de Compra'))

    return gad_purchase_doc


def get_gad_settings():
    """
    Get the gad settings document
    """
    gad_settings = frappe.get_doc("Gad Settings")

    if not gad_settings:
        frappe.throw(_('Por favor debe crear una Configuración'))

    return gad_settings


def get_template_url(field_name: str):
    """
    Get the template url from the gad settings document
    """
    gad_settings = get_gad_settings()
    template_url = gad_settings.get(field_name)

    if not template_url:
        frappe.throw(_('Por favor defina una plantilla en la Configuración'))

    return template_url


def get_docx_template_io(template_url: str):
    """
    Get the docx template as an IO object
    """

    path = os.path.join(
        get_files_path(is_private=True),
        os.path.basename(template_url),
    )

    with open(path, "rb") as fileobj:
        filedata = fileobj.read()

    return BytesIO(filedata)


def get_generated_docx(
        template_url: str,
        doc_name: str,
        template_field_name: str
):
    """
    Generate a docx document based on a template
    """
    template_io = get_docx_template_io(template_url)
    doc = DocxTemplate(template_io)
    document = get_gad_purchase_doc(doc_name)
    context_method = DOCUMENT_CONTEXT_MAPPING[template_field_name]
    context = context_method(document)
    doc.render(context)
    doc.save(GENERATED_DOCX_PATH)

    with open(GENERATED_DOCX_PATH, "rb") as output_file_obj:
        filedata = output_file_obj.read()

    return filedata


@frappe.whitelist()
def download_word(template_field_name: str, doc_name: str):
    """
    Generate a Word document based on a template and download it
    """
    template_url = get_template_url(template_field_name)
    filedata = get_generated_docx(
        template_url,
        doc_name,
        template_field_name,
    )

    frappe.local.response.filename = os.path.basename(template_url)
    frappe.local.response.filecontent = filedata
    frappe.local.response.type = "download"


INSTRUCTIONS = {
    'parts': [
        {
            'file': 'document'
        }
    ]
}


@frappe.whitelist()
def download_pdf(template_field_name: str, doc_name: str):
    """
    Generate a PDF document based on a template and download it
    """
    template_url = get_template_url(template_field_name)
    filedata = get_generated_docx(
        template_url,
        doc_name,
        template_field_name,
    )

    response = requests.request(
        'POST',
        'https://api.pspdfkit.com/build',
        headers={
            'Authorization': 'Bearer ' + PSPDF_KIT_API_KEY
        },
        files={
            'document': filedata
        },
        data={
            'instructions': json.dumps(INSTRUCTIONS)
        },
        stream=True
    )

    output_response = Response()
    if response.ok:
        output_response.headers['Content-Type'] = 'application/pdf'
        output_response.headers['Content-Disposition'] = 'inline; filename="output.pdf"'
        output_response.data = response.content
        return output_response

    frappe.throw(response.text)
    print(response.text)
    exit()
