# Copyright (c) 2025, Ecosoft and contributors
# For license information, please see license.txt


import frappe
from frappe import _
from frappe.query_builder import CustomFunction, functions as fn

def execute(filters=None):
    if filters.get("tree_type") and filters.get("range"):
        columns, data = get_pivot_grouped_data(filters)
    else:
        columns, data = get_regular_columns(), get_regular_data(filters)

    return columns, data, None, None, None

def get_regular_columns():
    return [
        {"label": _("ID"), "fieldname": "id", "fieldtype": "Link", "options": "Expense Claim", "width": 150},
        {"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 100},
        {"label": _("Grand Total"), "fieldname": "grand_total", "fieldtype": "Currency", "width": 120},
        {"label": _("Employee Name"), "fieldname": "employee_name", "fieldtype": "Data", "width": 150},
        {"label": _("Posting Date"), "fieldname": "posting_date", "fieldtype": "Date", "width": 120},
        {"label": _("Expense Date"), "fieldname": "expense_date", "fieldtype": "Date", "width": 120},
        {"label": _("Expense Claim Type"), "fieldname": "expense_type", "fieldtype": "Data", "width": 150},
        {"label": _("Description"), "fieldname": "description", "fieldtype": "Data", "width": 150},
        {"label": _("Default Account"), "fieldname": "default_account", "fieldtype": "Data", "width": 150},
        {"label": _("Supplier"), "fieldname": "supplier_name", "fieldtype": "Data", "width": 150},
        {"label": _("Customer"), "fieldname": "customer_name", "fieldtype": "Data", "width": 150},
        {"label": _("Shipping"), "fieldname": "shipping", "fieldtype": "Data", "width": 150},
        {"label": _("Amount"), "fieldname": "amount", "fieldtype": "Currency", "width": 120},
        {"label": _("Tax Amount"), "fieldname": "tax_amount", "fieldtype": "Currency", "width": 120},
        {"label": _("Total"), "fieldname": "total", "fieldtype": "Currency", "width": 120},
        {"label": _("Tax Invoice Number"), "fieldname": "tax_invoice_number", "fieldtype": "Data", "width": 150},
        {"label": _("Tax Invoice Date"), "fieldname": "tax_invoice_date", "fieldtype": "Date", "width": 120},
        {"label": _("Created By"), "fieldname": "create_by", "fieldtype": "Data", "width": 150},
        {"label": _("Created On"), "fieldname": "create_on", "fieldtype": "Datetime", "width": 150},
    ]

def get_regular_data(filters):
    tinv = frappe.qb.DocType("Expense Claim")
    tinvd = frappe.qb.DocType("Expense Claim Detail")
    sup = frappe.qb.DocType("Supplier")
    cust = frappe.qb.DocType("Customer")
    usr = frappe.qb.DocType("User")

    round_func = CustomFunction("round", ["value", "digit"])

    query = (
        frappe.qb.from_(tinv)
        .left_join(tinvd).on(tinvd.parent == tinv.name)  
        .left_join(sup).on(sup.name == tinv.supplier)  
        .left_join(cust).on(cust.name == tinvd.custom_customer)  
        .left_join(usr).on(usr.name == tinv.owner)
        .select(
            tinv.name.as_("id"),
            tinv.status.as_("status"),
            tinv.grand_total.as_("grand_total"),
            tinv.employee_name.as_("employee_name"),
            tinv.posting_date.as_("posting_date"),
            tinvd.expense_date.as_("expense_date"),
            tinvd.expense_type.as_("expense_type"),
            tinvd.description.as_("description"),
            tinvd.default_account.as_("default_account"),
            sup.supplier_name.as_("supplier_name"),
            cust.customer_name.as_("customer_name"),
            tinvd.custom_shipping.as_("shipping"),
            tinvd.amount.as_("amount"),
            round_func(tinv.total_taxes_and_charges, 2).as_("tax_amount"),
            round_func(tinvd.amount + tinv.total_taxes_and_charges, 2).as_("total"),
            tinv.tax_invoice_number.as_("tax_invoice_number"),
            tinv.tax_invoice_date.as_("tax_invoice_date"),
            usr.full_name.as_("create_by"),
            tinv.creation.as_("create_on"),
        )
        .where(tinv.docstatus.isin([1, 2]))
    )

    if filters.get("from_date"):
        query = query.where(tinv.posting_date >= filters["from_date"])
    if filters.get("to_date"):
        query = query.where(tinv.posting_date <= filters["to_date"])

    return query.run(as_dict=True)

def get_pivot_grouped_data(filters):
    tinv = frappe.qb.DocType("Expense Claim")
    tinvd = frappe.qb.DocType("Expense Claim Detail")

    range_fields = {
        "Weekly": CustomFunction("WEEK", ["date", "mode"])(tinv.posting_date, 1),
        "Monthly": CustomFunction("MONTH", ["date"])(tinv.posting_date),
        "Quarterly": CustomFunction("QUARTER", ["date"])(tinv.posting_date),
        "Yearly": CustomFunction("YEAR", ["date"])(tinv.posting_date),
    }

    range_field = range_fields.get(filters.get("range"))
    if not range_field:
        return [], []

    tree_type_mapping = {
        "Expense Claim": (tinv.name, "expense_claim"),
        "Employee": (tinv.employee_name, "employee_name"),
        "Expense Claim Type": (tinvd.expense_type, "expense_type"),
        "Account": (tinvd.default_account, "account"),
        "Supplier": (tinv.supplier, "supplier_name"),
        "Customer": (tinvd.custom_customer, "customer_name"),
        "Shipping": (tinvd.custom_shipping, "shipping"),
    }

    if filters.get("tree_type") in tree_type_mapping:
        group_by_field, alias = tree_type_mapping[filters["tree_type"]]
    else:
        group_by_field, alias = tinv.name, "expense_claim"

    columns = [
        {"label": _(alias.replace("_", " ").title()), "fieldname": alias, "fieldtype": "Data", "width": 150}
    ]

    query = (
        frappe.qb.from_(tinv)
        .left_join(tinvd).on(tinvd.parent == tinv.name)
        .select(
            group_by_field.as_(alias),
            range_field.as_("time_period"),
            fn.Sum(tinvd.amount).as_("sum_amount"),
            fn.Sum(tinv.total_taxes_and_charges).as_("sum_tax_amount"),
            fn.Sum(tinvd.amount + tinv.total_taxes_and_charges).as_("sum_total"),
        )
        .where(tinv.docstatus.isin([1, 2]))
        .groupby(group_by_field, range_field)
    )

    apply_date_filter(query, filters)

    raw_data = query.run(as_dict=True)

    time_periods = sorted(set(d["time_period"] for d in raw_data))

    for period in time_periods:
        columns.append({"label": f"{filters['range']} {period}", "fieldname": f"time_{period}", "fieldtype": "Currency", "width": 120})

    pivot_data = {}
    for group in raw_data:
        key = group[alias]
        if key not in pivot_data:
            pivot_data[key] = {alias: key}

        pivot_data[key][f"time_{group['time_period']}"] = group["sum_amount"]

    return columns, list(pivot_data.values())

def apply_date_filter(query, filters):
    tinv = frappe.qb.DocType("Expense Claim")
    if filters.get("from_date") and filters.get("to_date"):
        query = query.where((tinv.posting_date >= filters["from_date"]) & (tinv.posting_date <= filters["to_date"]))
    elif filters.get("from_date"):
        query = query.where(tinv.posting_date >= filters["from_date"])
    elif filters.get("to_date"):
        query = query.where(tinv.posting_date <= filters["to_date"])
