import frappe
from erpnext.selling.doctype.sales_order.sales_order import SalesOrder

class CustomlinkSalesOrder(SalesOrder):
    def on_cancel(self):
        self.flags.ignore_links = True
        super().on_cancel()
