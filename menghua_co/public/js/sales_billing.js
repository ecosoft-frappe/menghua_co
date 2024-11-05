frappe.ui.form.on('Sales Billing', {
    refresh(frm) {
        if (frm.doc.docstatus === 1 && frm.doc.outstanding_amount !== 0) {
            frm.add_custom_button(__('Payment'), function() {
                frappe.call({
                    method: "menghua_co.custom.sales_billing.create_payment_entry",
                    args: {
                        sales_billing: frm.doc.name  
                    },
                });
            }, __("Action"));
            frm.page.set_inner_btn_group_as_primary(__('Action'));
        }
    }
});
