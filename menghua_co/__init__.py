__version__ = "0.0.1"

# Monkey patching
# ------------------

import frappe
from erpnext.selling.doctype.quotation import quotation

original_make_sales_order = quotation._make_sales_order


def _make_sales_order(source_name, target_doc=None, ignore_permissions=False):
    sale_order = original_make_sales_order(source_name, target_doc=target_doc, ignore_permissions=ignore_permissions)
    quotation = frappe.get_doc("Quotation", source_name)
    # Update fields on sales order doctype
    sale_order.delivery_date = quotation.custom_delivery_date
    for item in sale_order.items:
        item.delivery_date = sale_order.delivery_date
    return sale_order


quotation._make_sales_order = _make_sales_order
