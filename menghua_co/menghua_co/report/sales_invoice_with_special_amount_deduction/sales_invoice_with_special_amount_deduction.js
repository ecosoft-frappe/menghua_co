// Copyright (c) 2025, Ecosoft and contributors
// For license information, please see license.txt

frappe.query_reports["Sales Invoice With Special Amount Deduction"] = {
	"filters": [
		{
			label: __("From Due Date"),
			fieldname: "from_due_date",
			fieldtype: "Date",
			default: frappe.datetime.month_start(),
		},
		{
			label: __("To Due Date"),
			fieldname: "to_due_date",
			fieldtype: "Date",
			default: frappe.datetime.month_end(),
		},
		{
			label: __("Customer"),
			fieldname: "customer",
			fieldtype: "Link",
			options: "Customer",
		},
		{
			label: __("Sales Person"),
			fieldname: "sales_person",
			fieldtype: "Link",
			options: "Sales Person",
		},
		{
			label: __("Sales Order"),
			fieldname: "sales_order",
			fieldtype: "Link",
			options: "Sales Order",
		},
		{
			label: __("Show Paid Invoice Only"),
			fieldname: "paid_only",
			fieldtype: "Check",
			default: 0,
		}
	]
};
