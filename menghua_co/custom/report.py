import frappe

def set_report_as_disable():
    reports = [
        "Accounts Receivable Summary",
    ]
    for report in reports:
        frappe.db.set_value("Report", report, "disabled", 1)
