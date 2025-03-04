import frappe
from frappe import _, throw
from frappe.utils import get_link_to_form
from erpnext.accounts.doctype.purchase_invoice.purchase_invoice import PurchaseInvoice


class PurchaseInvoiceMH(PurchaseInvoice):

    # Overwrite
    def po_required(self):
        if frappe.db.get_value("Buying Settings", None, "po_required") == "Yes":
            if frappe.get_value(
                "Supplier", self.supplier, "allow_purchase_invoice_creation_without_purchase_order"
            ):
                return

            for d in self.get("items"):
                if not d.purchase_order:
                    msg = _("You must create a Purchase Order before adding Item {}").format(frappe.bold(d.item_code))
                    msg += "<br><br>"
                    msg += _(
                        "To submit the invoice without purchase order please set {0} as {1} in {2}"
                    ).format(
                        frappe.bold(_("Purchase Order Required")),
                        frappe.bold(_("No")),
                        get_link_to_form("Buying Settings", "Buying Settings", "Buying Settings"),
                    )
                    throw(msg, title=_("Mandatory Purchase Order"))

    # Overwrite
    def pr_required(self):
        stock_items = self.get_stock_items()
        if frappe.db.get_value("Buying Settings", None, "pr_required") == "Yes":
            if frappe.get_value(
                "Supplier", self.supplier, "allow_purchase_invoice_creation_without_purchase_receipt"
            ):
                return

            for d in self.get("items"):
                if not d.purchase_receipt and d.item_code in stock_items:
                    msg = _("You must create a Purchase Receipt before adding Item {}").format(frappe.bold(d.item_code))
                    msg += "<br><br>"
                    msg += _(
                        "To submit the invoice without purchase receipt please set {0} as {1} in {2}"
                    ).format(
                        frappe.bold(_("Purchase Receipt Required")),
                        frappe.bold(_("No")),
                        get_link_to_form("Buying Settings", "Buying Settings", "Buying Settings"),
                    )
                    throw(msg, title=_("Mandatory Purchase Receipt"))
