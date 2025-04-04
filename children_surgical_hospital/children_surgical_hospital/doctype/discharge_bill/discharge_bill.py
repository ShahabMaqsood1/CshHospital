# Copyright (c) 2025, Shahab Maqsood and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class DischargeBill(Document):
    def before_insert(self):
        if not self.receptionist:
            user_full_name = frappe.db.get_value("User", frappe.session.user, "full_name")
            self.receptionist = user_full_name
