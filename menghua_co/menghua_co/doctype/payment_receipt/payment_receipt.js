frappe.ui.form.on('Payment Receipt', {
    customer: function(frm) {
        if (frm.doc.customer) {
            frm.set_query('sales_billing', function() {
                return {
                    filters: {
                        "customer": frm.doc.customer
                    }
                };
            });
        }
    },
    
    sales_billing: function(frm) {
        if (frm.doc.sales_billing) {
            frm.events.get_documents_from_sales_billing(frm, { "sales_billing": frm.doc.sales_billing, "allocate_payment_amount": 1 });
        }
    },

    get_documents_from_sales_billing: function(frm, filters) {
        frm.clear_table("references");
        frm.refresh_field("references");

        if (!frm.doc.customer || !frm.doc.sales_billing) {
            frappe.msgprint(__("Customer and Sales Billing must be selected."));
            return;
        }

        var sales_billing = filters["sales_billing"];
        frm.set_value("sales_billing", sales_billing);
        frappe.flags.allocate_payment_amount = filters["allocate_payment_amount"];

        frappe.db.get_doc("Sales Billing", sales_billing).then(bill => {
            console.log("Sales Billing Document:", bill);

            if (!bill.sales_billing_line || !bill.sales_billing_line.length) {
                frappe.msgprint(__("No sales billing lines found in the selected Sales Billing."));
                return;
            }

            var invoices = [];
            $.each(bill.sales_billing_line, function(i, d) {
                if (d.sales_invoice) {
                    invoices.push(d.sales_invoice);
                }
            });

            if (!invoices.length) {
                frappe.msgprint(__("No Sales Invoice linked to the selected Sales Billing."));
                return;
            }

            console.log("Invoices to Fetch:", invoices);

            frappe.db.get_list("Sales Invoice", {
                fields: ["*"],
                filters: {
                    name: ["in", invoices]
                }
            }).then(records => {
                console.log("Sales Invoice Records:", records);

                if (!records || !records.length) {
                    frappe.msgprint(__("No Sales Invoice records found for the selected Sales Billing."));
                    return;
                }

                var voucher_type = "Sales Invoice";

                $.each(records, function(i, d) {
                    var c = frm.add_child("references");
                    c.reference_doctype = voucher_type;
                    c.reference_name = d.name;
                    c.due_date = d.due_date;
                    c.total_amount = d.grand_total;

                });
                frm.refresh_field("references");
            });
        });
    }
});

frappe.ui.form.on('Payment Receipt', {
    onload: function (frm) {
        frm.fields_dict['payment_entry'].grid.get_field('payment_entry').get_query = function (doc, cdt, cdn) {
            const customer = frm.doc.customer;
            return {
                filters: {
                    'party': customer,       
                    'party_type': 'Customer' 
                }
            };
        };
    }
});

