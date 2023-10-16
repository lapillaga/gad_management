import frappe
from frappe import _


def get_gad_payment_justification_doc(doc_name: str):
    """
    Get the GAD Payment Justification document
    """
    gad_memo_doc = frappe.get_doc("Gad Payment Justification", doc_name)

    if not gad_memo_doc:
        frappe.throw(_('El Justificativo de Pago no existe'))
    return gad_memo_doc
