frappe.ui.form.on('Sales Billing', {
    refresh: function(frm) {
        frm.add_custom_button(__('Payment'), function() {
            frm.events.create_payment_entry(frm);
        }, __('Action'));
        frm.page.set_inner_btn_group_as_primary(__('Action'));
    },

    create_payment_entry: function(frm) {
        frappe.call({
            method: 'menghua_co.custom.sales_billing.create_payment_entry',  
            args: {
                sales_billing_name: frm.doc.name
            },
            callback: function(r) {
                if (r.message) {
                    frappe.set_route('Form', 'Payment Entry', r.message);
                }
            }
        });
        
    }
});
