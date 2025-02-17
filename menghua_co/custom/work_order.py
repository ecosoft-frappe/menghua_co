import frappe
from frappe import _
from frappe.model.mapper import get_mapped_doc
from frappe.model.document import Document

class WorkOrder(Document):
    def after_insert(self):
        auto_create_manufacturing_order(self)

@frappe.whitelist()
def auto_create_manufacturing_order(work_order, method=None):
    if work_order.sales_order:
        auto_mo_from_so = frappe.get_cached_value("Company", work_order.company, "auto_mo_from_so")
        if auto_mo_from_so == 1:
            create_manufacturing_order(work_order.name, show_message=False)
    
    elif work_order.material_request:
        auto_mo_from_mr = frappe.get_cached_value("Company", work_order.company, "auto_mo_from_mr")
        if auto_mo_from_mr == 1:
            create_manufacturing_order(work_order.name, show_message=False)

@frappe.whitelist()
def create_manufacturing_order(source_name, target_doc=None, show_message=True): 
    def set_missing_values(source, target):
        target.date = source.creation
        target.company = source.company
        target.sales_order = source.sales_order or None
        target.item_code = source.production_item or None
        target.item_name = source.item_name or None
        target.quantity = source.qty or 0
        target.uom = source.stock_uom or None
        target.customer = None
        target.delivery_date = None
        target.shipping = None

        if source.sales_order:
            sales_order = frappe.get_doc("Sales Order", source.sales_order)
            target.customer = getattr(sales_order, "customer", None)
            target.delivery_date = getattr(sales_order, "delivery_date", None)
            target.shipping = getattr(sales_order, "custom_shipping", None)

            if not target.get("sales_team"):
                for d in sales_order.get("sales_team") or []:
                    target.append(
                        "sales_team",
                        {
                            "sales_person": d.sales_person,
                            "allocated_percentage": d.allocated_percentage or None,
                            "allocated_amount": d.allocated_amount or None,
                            "commission_rate": d.commission_rate or None,
                            "incentives": d.incentives or None,
                        },
                    )

        if source.material_request:
            material_request = frappe.get_doc("Material Request", source.material_request)
            target.customer = getattr(material_request, "customer", None)
            target.delivery_date = getattr(material_request, "delivery_date", source.creation)

    doc = get_mapped_doc(
        "Work Order", 
        source_name, 
        {
            "Work Order": {  
                "doctype": "Manufacturing Order", 
            }
        },
        target_doc, 
        set_missing_values, 
    )

    if doc:
        new_doc = doc.insert()  
        if show_message:
            frappe.msgprint(
                _("Manufacturing Order Created: <a href='/app/manufacturing-order/{0}'>{0}</a>").format(new_doc.name),
                alert=True,
                indicator="green"
            )
