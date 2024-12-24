import frappe

def set_created_by_full_name(doc, method):
    user = frappe.session.user
    user_doc = frappe.get_doc("User", user)
    doc.created_by = user_doc.full_name