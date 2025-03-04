import frappe
from frappe import _
from erpnext.stock.doctype.purchase_receipt.purchase_receipt import PurchaseReceipt


class PurchaseReceiptMH(PurchaseReceipt):

    # Overwrite
    def po_required(self):
        if frappe.db.get_value("Buying Settings", None, "po_required") == "Yes":
            for d in self.get("items"):
                if not d.purchase_order:
                    frappe.throw(_("You must create a Purchase Order before adding Item {0}").format(d.item_code))
