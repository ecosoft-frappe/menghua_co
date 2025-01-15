frappe.ui.form.on("Sales Order", {
    refresh(frm) {
        frm.set_query("custom_shipping", function () {
            return {
                filters: {
                    'is_transporter': 1 
                }
            };
        });
    }
});