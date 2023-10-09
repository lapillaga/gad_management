import frappe
from frappe import _


def get_gad_memo_template_doc(doc_name: str):
    """
    Get the GAD Memo Template document
    """
    gad_memo_template_doc = frappe.get_doc("Gad Memo Template", doc_name)

    if not gad_memo_template_doc:
        frappe.throw(_('Por favor debe crear una Plantilla Memo'))
    return gad_memo_template_doc
