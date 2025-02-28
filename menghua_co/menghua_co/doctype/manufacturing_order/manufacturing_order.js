// Copyright (c) 2024, Ecosoft and contributors
// For license information, please see license.txt

frappe.ui.form.on("Manufacturing Order", {
    onload: function(frm) {
        if (frm.doc.docstatus == 0 && frm.doc.mh_status == "ยกเลิก") {
            frm.set_value("mh_status", "ร่าง");
        }
    },
    validate: function(frm) {
        if (frm.doc.docstatus == 0 && frm.doc.mh_status == "ยกเลิก") {
            frm.set_value("mh_status", "ร่าง");
        }
    },
    refresh: function (frm) {
        if (frm.doc.docstatus === 1) {
            frm.toggle_display("sales_team_section", true);
        } else if (frm.doc.sales_order) {
            frappe.call({
                method: "frappe.client.get",
                args: {
                    doctype: "Sales Order",
                    name: frm.doc.sales_order,
                },
                callback: function (r) {
                    if (r.message) {
                        let sales_order = r.message;
                        if (sales_order.sales_team && sales_order.sales_team.length > 0) {
                            frm.toggle_display("sales_team_section", false);
                        } else {
                            frm.toggle_display("sales_team_section", true);
                        }
                    }
                },
            });
        } else {
            frm.toggle_display("sales_team_section", true);
        }
    },
    customer: function(frm) {
        frm.set_query("sales_order", function() {
            return {
                filters: {
                    "customer": frm.doc.customer
                }
            };
        });
    },
    coating: function(frm) {
        frm.set_value("coating_detail", "");
    }
});
