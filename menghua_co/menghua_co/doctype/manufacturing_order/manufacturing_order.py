# Copyright (c) 2024, Ecosoft and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ManufacturingOrder(Document):
    def before_submit(self):
        if self.mh_status == "ร่าง":
            self.mh_status = "รอผลิต"
            
    def on_cancel(self):
        self.mh_status = "ยกเลิก"
        self.db_update()