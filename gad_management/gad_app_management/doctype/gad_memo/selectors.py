import frappe
from frappe import _


def get_gad_memo_doc(doc_name: str):
    """
    Get the GAD Memo document
    """
    gad_memo_doc = frappe.get_doc("Gad Memo", doc_name)

    if not gad_memo_doc:
        frappe.throw(_('Por favor debe crear un Memo'))
    return gad_memo_doc
