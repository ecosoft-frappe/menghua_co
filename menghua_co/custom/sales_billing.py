import frappe
from frappe import _
from erpnext.accounts.party import get_party_account
from erpnext.accounts.doctype.payment_entry.payment_entry import get_payment_entry

@frappe.whitelist()
def make_payment_entry(source_name, target_doc=None):
    from frappe.model.mapper import get_mapped_doc

    def set_missing_values(source, target):
        target.payment_type = "Receive" 
        target.party_type = "Customer" 
        target.party = source.customer 
        target.party_name = source.customer_name
        target.paid_to = frappe.get_value("Company", source.company, "default_bank_account")
        target.paid_from = get_party_account("Customer", source.customer, source.company)
        target.paid_amount = source.total_billing_amount
        target.received_amount = target.paid_amount

        for line in source.sales_billing_line:
            if line.sales_invoice:  
                target.append(
                    "references",
                    dict(
                        reference_doctype="Sales Invoice",  
                        reference_name=line.sales_invoice,  
                        total_amount=line.grand_total,
                        allocated_amount=source.total_billing_amount,
                        paid_amount=line.outstanding_amount,  
                        outstanding_amount=line.outstanding_amount,
                    ),
                )

    doclist = get_mapped_doc(
        "Sales Billing",  
        source_name,  
        {
            "Sales Billing": {
                "doctype": "Payment Entry",  
                "validation": {"docstatus": ["=", 1]},  
                "field_no_map": ["naming_series"],
            }
        },
        target_doc, 
        set_missing_values,
    )

    return doclist

