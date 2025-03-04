import frappe
from frappe import _, msgprint
from erpnext.accounts.doctype.sales_invoice.sales_invoice import SalesInvoice


class SalesInvoiceMH(SalesInvoice):

    # Overwrite
    def so_dn_required(self):
        """check in manage account if sales order / delivery note required or not."""
        if self.is_return:
            return

        prev_doc_field_map = {
            "Sales Order": ["so_required", "is_pos"],
            "Delivery Note": ["dn_required", "update_stock"],
        }
        for key, value in prev_doc_field_map.items():
            if frappe.db.get_single_value("Selling Settings", value[0]) == "Yes":
                if frappe.get_value("Customer", self.customer, value[0]):
                    continue

                for d in self.get("items"):
                    if d.item_code and not d.get(key.lower().replace(" ", "_")) and not self.get(value[1]):
                        msgprint(
                            _("You must create a {0} before adding Item {1}").format(key, d.item_code), raise_exception=1
                        )
