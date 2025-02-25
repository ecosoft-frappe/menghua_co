// Copyright (c) 2025, Ecosoft and contributors
// For license information, please see license.txt

frappe.query_reports["รายงานค่าใช้จ่ายแต่ละรายการ"] = {
	"filters": [
		{
			fieldname: "tree_type",
			label: __("Tree Type"),
			fieldtype: "Select",
			options: [
				"",
				"Expense Claim",
				"Employee",
				"Expense Claim Type",
				"Account",
				"Supplier",
				"Customer",
				"Shipping",
			],
			default: " ",
			reqd: 0,
		},
		{
			fieldname: "range",
			label: __("Range"),
			fieldtype: "Select",
			options: [
				{ value: "", label: __(" ") },
				{ value: "Weekly", label: __("Weekly") },
				{ value: "Monthly", label: __("Monthly") },
				{ value: "Quarterly", label: __("Quarterly") },
				{ value: "Yearly", label: __("Yearly") },
			],
			default: "",
			reqd: 0,  
		},
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
		},
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			default: frappe.defaults.get_user_default("Company"),
			reqd: 1,
		},	
	],
};
