import frappe
from frappe.utils import cint

from erpnext.accounts.doctype.sales_invoice.sales_invoice import SalesInvoice
from erpnext.selling.doctype.sales_order.sales_order import SalesOrder
from erpnext.accounts.doctype.purchase_invoice.purchase_invoice import PurchaseInvoice
from erpnext.stock.doctype.purchase_receipt.purchase_receipt import PurchaseReceipt
from erpnext.buying.doctype.purchase_order.purchase_order import PurchaseOrder
from erpnext.buying.doctype.supplier_quotation.supplier_quotation import SupplierQuotation
from erpnext.stock.doctype.delivery_note.delivery_note import DeliveryNote

def validate_with_bypass_validate(doc):
    bypass_validate = frappe.db.get_value("Company", doc.company, "bypass_previous_doc_validation")
    return cint(bypass_validate) != 1

class CustomDocument:
    def validate_with_previous_doc(self):
        if validate_with_bypass_validate(self):
            super().validate_with_previous_doc()

class CustomSalesInvoice(CustomDocument, SalesInvoice):
    pass

class CustomSalesOrder(CustomDocument, SalesOrder):
    pass

class CustomPurchaseInvoice(CustomDocument, PurchaseInvoice):
    pass

class CustomPurchaseReceipt(CustomDocument, PurchaseReceipt):
    pass

class CustomPurchaseOrder(CustomDocument, PurchaseOrder):
    pass

class CustomSupplierQuotation(CustomDocument, SupplierQuotation):
    pass

class CustomDeliveryNote(CustomDocument, DeliveryNote):
    pass
