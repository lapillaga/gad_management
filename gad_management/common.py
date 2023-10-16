import frappe
import os

from frappe import _
from io import BytesIO
from frappe.utils import get_files_path


GENERATED_DOCX_PATH = '/tmp/generated.docx'


def get_gad_settings():
    """
    Get the gad settings document
    """
    gad_settings = frappe.get_doc("Gad Settings")

    if not gad_settings:
        frappe.throw(_('Por favor debe crear una Configuración'))

    return gad_settings


def get_template_url_from_settings(field_name: str):
    """
    Get the template url from the gad settings document
    """
    gad_settings = get_gad_settings()
    template_url = gad_settings.get(field_name)

    if not template_url:
        frappe.throw(_('Por favor defina una plantilla en la Configuración'))

    return template_url


def get_docx_template_io(template_url: str, is_private: bool = True):
    """
    Get the docx template as an IO object
    """

    path = os.path.join(
        get_files_path(is_private=is_private),
        os.path.basename(template_url),
    )

    with open(path, "rb") as fileobj:
        filedata = fileobj.read()

    return BytesIO(filedata)


def generate_file_response(
        filedata: bytes,
        template_url: str,
        filename: str = None,
):
    """
    Generate a file response
    """
    frappe.local.response.filename = (
        os.path.basename(template_url)
        if not filename
        else filename
    )
    frappe.local.response.filecontent = filedata
    frappe.local.response.type = "download"
