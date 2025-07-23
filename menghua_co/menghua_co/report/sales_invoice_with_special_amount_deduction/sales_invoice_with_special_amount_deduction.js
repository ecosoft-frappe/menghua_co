// Copyright (c) 2025, Ecosoft and contributors
// For license information, please see license.txt

frappe.query_reports["Sales Invoice With Special Amount Deduction"] = {
	"filters": [
		{
			label: __("From Date"),
			fieldname: "from_date",
			fieldtype: "Date",
			reqd: 1,
		},
		{
			label: __("To Date"),
			fieldname: "to_date",
			fieldtype: "Date",
			reqd: 1,
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
