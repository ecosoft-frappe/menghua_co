// Copyright (c) 2024, Ecosoft and contributors
// For license information, please see license.txt

frappe.ui.form.on('Manufacturing Order', {
    customer: function(frm) {
        frm.set_query('sales_order', function() {
            return {
                filters: {
                    'customer': frm.doc.customer
                }
            };
        });
    }
});

