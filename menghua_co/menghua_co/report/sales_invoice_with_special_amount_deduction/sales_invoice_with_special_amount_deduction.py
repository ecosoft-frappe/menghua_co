# Copyright (c) 2025, Ecosoft and contributors
# For license information, please see license.txt

import frappe
from frappe import _ 


def execute(filters=None):
    if not filters:
        filters = {}
    
    columns = get_columns()
    data = get_data(filters)
    
    return columns, data

def get_columns():
    return [
        {
            "fieldname": "customer",
            "label": _("Customer"),
            "fieldtype": "Link",
            "options": "Customer",
            "width": 200
        },
        {
            "fieldname": "sales_person",
            "label": _("Sales Person"),
            "fieldtype": "Link",
            "options": "Sales Person",
            "width": 150
        },
        {
            "fieldname": "sales_invoice",
            "label": _("Sales Invoice"),
            "fieldtype": "Link",
            "options": "Sales Invoice",
            "width": 250
        },
        {
            "fieldname": "sales_invoice_url",
            "label": _("Sales Invoice URL"),
            "fieldtype": "Html",
            "width": 0
        },
        {
            "fieldname": "ref_sales_order",
            "label": _("Ref Sales Order"),
            "fieldtype": "Link",
            "options": "Sales Order",
            "width": 250
        },
        {
            "fieldname": "invoice_amount_net",
            "label": _("Invoice Amount (Net)"),
            "fieldtype": "Currency",
            "width": 0
        },
        {
            "fieldname": "discount_special_1",
            "label": _("Discount (Special 1)"),
            "fieldtype": "Currency",
            "width": 0
        },
        {
            "fieldname": "remarks_special_amount_1",
            "label": _("Remark Discount (Special 1)"),
            "fieldtype": "Data",
            "width": 0
        },
        {
            "fieldname": "contribution_special_2",
            "label": _("Contribution (Special 2)"),
            "fieldtype": "Currency",
            "width": 0
        },
        {
            "fieldname": "remarks_special_amount_2",
            "label": _("Remark Contribution (Special 2)"),
            "fieldtype": "Data",
            "width": 0
        },
        {
            "fieldname": "commission_special_3",
            "label": _("Commission (Special 3"),
            "fieldtype": "Currency",
            "width": 0
        },
        {
            "fieldname": "remarks_special_amount_3",
            "label": _("Remark Commission (Special 3"),
            "fieldtype": "Data",
            "width": 0
        },
        {
            "fieldname": "total_special_amounts",
            "label": _("Total Special Amounts"),
            "fieldtype": "Currency",
            "width": 0
        },
        {
            "fieldname": "net_amount",
            "label": _("Net Amount"),
            "fieldtype": "Currency",
            "width": 0
        },
        {
            "fieldname": "percent_decrease",
            "label": _("Percent Decrease"),
            "fieldtype": "Percent",
            "width": 0
        },
        {
            "fieldname": "due_date",
            "label": _("Due Date"),
            "fieldtype": "Date",
            "width": 110
        },
        {
            "fieldname": "paid_date",
            "label": _("Paid Date"),
            "fieldtype": "Date",
            "width": 110
        },
        {
            "fieldname": "days_overdue",
            "label": _("Days Overdue"),
            "fieldtype": "Int",
            "width": 0
        }
    ]

def get_data(filters):

    base_url = frappe.utils.get_url()

    query_filters = ["si.docstatus = 1"]
    values = {}

    if filters.get("from_due_date"):
        query_filters.append("si.due_date >= %(from_due_date)s")
        values["from_due_date"] = filters["from_due_date"]

    if filters.get("to_due_date"):
        query_filters.append("si.due_date <= %(to_due_date)s")
        values["to_due_date"] = filters["to_due_date"]

    if filters.get("customer"):
        query_filters.append("si.customer = %(customer)s")
        values["customer"] = filters["customer"]

    if filters.get("sales_person"):
        query_filters.append("st.sales_person = %(sales_person)s")
        values["sales_person"] = filters["sales_person"]

    if filters.get("sales_order"):
        query_filters.append("sii.sales_order = %(sales_order)s")
        values["sales_order"] = filters["sales_order"]

    if filters.get("paid_only"):
        query_filters.append("si.status = 'Paid'")

    conditions = " AND ".join(query_filters)

    query = f"""
        SELECT 
            si.customer,
            GROUP_CONCAT(DISTINCT st.sales_person ORDER BY st.sales_person SEPARATOR ', ') AS sales_person,
            si.name AS sales_invoice,
            CONCAT('{base_url}/app/sales-invoice/', si.name) AS sales_invoice_url,
            GROUP_CONCAT(DISTINCT sii.sales_order ORDER BY sii.sales_order SEPARATOR ', ') AS ref_sales_order,
            si.net_total AS invoice_amount_net,
            IFNULL(si.custom_special_amount_1_discount, 0) AS discount_special_1,
            IFNULL(si.custom_remarks_special_amount_1, '') AS remarks_special_amount_1,
            IFNULL(si.custom_special_amount_2_contribution, 0) AS contribution_special_2,
            IFNULL(si.custom_remarks_special_amount_2, '') AS remarks_special_amount_2,
            IFNULL(si.custom_special_amount_3_commission, 0) AS commission_special_3,
            IFNULL(si.custom_remarks_special_amount_3, '') AS remarks_special_amount_3,
            (
                IFNULL(si.custom_special_amount_1_discount, 0)
                + IFNULL(si.custom_special_amount_2_contribution, 0)
                + IFNULL(si.custom_special_amount_3_commission, 0)
            ) AS total_special_amounts,
            (
                si.net_total 
                - IFNULL(si.custom_special_amount_1_discount, 0) 
                - IFNULL(si.custom_special_amount_2_contribution, 0)
            ) AS net_amount,
            CASE 
                WHEN si.net_total > 0 THEN 
                    ROUND(
                        (
                            (IFNULL(si.custom_special_amount_1_discount, 0) + IFNULL(si.custom_special_amount_2_contribution, 0))
                            * 100
                        ) / si.net_total, 2
                    )
                ELSE 0 
            END AS percent_decrease,
            si.due_date,
            paid.pe_date AS paid_date,
            CASE 
                WHEN si.status = 'Paid' THEN 
                    GREATEST(
                        DATEDIFF(
                            IFNULL(paid.pe_date, si.due_date),
                            si.due_date
                        ), 0
                    )
                WHEN si.status != 'Paid' 
                    AND si.due_date IS NOT NULL 
                    AND si.due_date < CURDATE() 
                THEN DATEDIFF(CURDATE(), si.due_date)
                ELSE 0 
            END AS days_overdue
        FROM `tabSales Invoice` si
        LEFT JOIN `tabSales Team` st 
            ON st.parent = si.name 
            AND st.parenttype = 'Sales Invoice' 
            AND st.parentfield = 'sales_team'
        LEFT JOIN `tabSales Invoice Item` sii 
            ON sii.parent = si.name
        LEFT JOIN (
            SELECT 
                per.reference_name,
                MAX(pe.posting_date) AS pe_date
            FROM `tabPayment Entry Reference` per
            JOIN `tabPayment Entry` pe ON pe.name = per.parent
            JOIN `tabSales Invoice` paid_invoice ON paid_invoice.name = per.reference_name
            WHERE per.reference_doctype = 'Sales Invoice'
                AND pe.docstatus = 1
                AND paid_invoice.status = 'Paid'
            GROUP BY per.reference_name
        ) paid ON paid.reference_name = si.name
        WHERE {conditions}
        GROUP BY si.name
        ORDER BY si.due_date ASC
    """

    return frappe.db.sql(query, values, as_dict=1)
