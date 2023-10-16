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


def get_gad_member_by_role(role: str):
    """
    Get the GAD Member document by role
    """
    gad_member_doc = frappe.get_list(
        "Gad Member",
        filters={"role": role},
        fields=[
            "name",
            "full_name",
            "role_name",
            "title",
        ],
    )

    if not gad_member_doc:
        frappe.throw(_(f'No existe un Miembro con el rol {role}'))

    return gad_member_doc[0]
