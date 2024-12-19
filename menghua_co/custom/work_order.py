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
        target.sales_order = source.sales_order
        target.item_code = source.production_item
        target.item_name = source.item_name
        target.quantity = source.qty
        target.uom = source.stock_uom
        
        if source.sales_order:
            sales_order = frappe.get_doc("Sales Order", source.sales_order)
    
        target.customer = sales_order.customer  
        target.delivery_date = sales_order.delivery_date
    
        if not target.get("sales_team"):
            for d in sales_order.get("sales_team") or []:
                target.append(
                "sales_team",
                {
                    "sales_person": d.sales_person,
                    "allocated_percentage": d.allocated_percentage or None,
                    "allocated_amount": d.allocated_amount,
                    "commission_rate": d.commission_rate,
                    "incentives": d.incentives,
                },
            )
                
        elif source.material_request:
            material_request = frappe.get_doc("Material Request", source.material_request)
            target.customer = material_request.customer  
            target.delivery_date = material_request.delivery_date if hasattr(material_request, 'delivery_date') else source.creation

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
