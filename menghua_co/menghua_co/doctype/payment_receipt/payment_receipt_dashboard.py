from frappe import _

def get_data():
    return {
        "fieldname": "payment_receipt", 
        "internal_and_external_links": {
			"Sales Invoice": ["references", "sales_invoice"],
            "Payment Entry": "payment_entry",
		},
        "transactions": [
            {"items": ["Sales Invoice", "Payment Entry"],}, 
        ],
    }
