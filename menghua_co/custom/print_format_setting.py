import frappe

def set_print_format_as_disable():
    print_formats = [
        "Point of Sale",
        "Sales Invoice Return",
        "Bank and Cash Payment Voucher",
        "Drop Shipping Format",
        "Sales Auditing Voucher",
        "Purchase Receipt Serial and Batch Bundle Print",
        "Purchase Receipt MH",
        "Delivery Note MH",  # Disable form temporary
        "Receipt in Payment Entry MH",
    ]
    for print_format in print_formats:
        frappe.db.set_value("Print Format", print_format, "disabled", 1)

def set_print_format_as_add_comment():
    print_formats = frappe.get_list("Print Format", filters={"module": "Menghua Co"}, pluck="name")
    for print_format in print_formats:
        frappe.db.set_value("Print Format", print_format, "add_comment_info", 1)
