import frappe
from frappe import _
from erpnext.stock.doctype.delivery_note.delivery_note import DeliveryNote


class DeliveryNoteMH(DeliveryNote):

    # Overwrite
    def so_required(self):
        """check in manage account if sales order required or not"""
        if frappe.db.get_single_value("Selling Settings", "so_required") == "Yes":
            for d in self.get("items"):
                if not d.against_sales_order:
                    frappe.throw(_("You must create a Sales Order before adding Item {0}").format(d.item_code))
