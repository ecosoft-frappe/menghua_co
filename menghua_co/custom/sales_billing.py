import frappe
from frappe import _
from erpnext.accounts.doctype.payment_entry.payment_entry import get_payment_entry

@frappe.whitelist()
def create_payment_entry(sales_billing_name):
    sales_billing = frappe.get_doc("Sales Billing", sales_billing_name)
    
    payment_entry = frappe.new_doc("Payment Entry")
    payment_entry.payment_type = "Receive"
    payment_entry.party_type = "Customer"
    payment_entry.party = sales_billing.customer
    payment_entry.party_name = sales_billing.customer_name
    payment_entry.paid_amount = sales_billing.total_billing_amount 
    payment_entry.received_amount = sales_billing.total_billing_amount 
    payment_entry.paid_to = sales_billing.total_billing_amount

    payment_entry.insert()
    return payment_entry.name