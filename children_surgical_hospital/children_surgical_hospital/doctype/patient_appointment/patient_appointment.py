# Copyright (c) 2024, Shahab Maqsood and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class PatientAppointment(Document):
    def before_insert(self):
        if not self.receptionist:
            user_full_name = frappe.db.get_value("User", frappe.session.user, "full_name")
            self.receptionist = user_full_name

    def before_save(self):
        if not self.status:
            frappe.throw("The status field must not be empty.")

        if self.status not in ["Scheduled", "Completed", "Cancelled"]:
            frappe.throw(f"Invalid status value: {self.status}. Must be one of 'Scheduled', 'Completed', or 'Cancelled'.")

        # Ensure the status update is allowed after submission
        self.flags.ignore_validate_update_after_submit = True

        # Auto-create Patient Record only if patient_id is empty
        if not self.patient_id:
            new_patient = frappe.get_doc({
                "doctype": "Patient Record",
                "patient_name": self.patient_name,
                "age": self.age,
                "gender": self.gender,
                "weight": self.weight,
                "contact_number": self.phone_number,  
                "father_name": self.father_name,
                "cnic": self.cnic,
                "address": self.address
            })
            new_patient.insert(ignore_permissions=True)

            # Assign the new patient_id to the appointment
            self.patient_id = new_patient.name
            frappe.msgprint(f"New patient created: {new_patient.name}", alert=True)