import frappe
from frappe import _


def get_gad_member_doc(doc_name: str):
    """
    Get the GAD Member document
    """
    gad_memo_doc = frappe.get_doc("Gad Member", doc_name)

    if not gad_memo_doc:
        frappe.throw(_(f'No existe un Miembro con el nombre {doc_name}'))
    return gad_memo_doc
