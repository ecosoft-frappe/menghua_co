import frappe

def set_print_format_as_disable():
    print_formats = [
        "Point of Sale",
        "Sales Invoice Return",
        "Bank and Cash Payment Voucher",
        "Drop Shipping Format",
        "Sales Auditing Voucher",
        "Purchase Receipt Serial and Batch Bundle Print",
    ]
    for print_format in print_formats:
        frappe.db.set_value("Print Format", print_format, "disabled", 1)