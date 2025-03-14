import frappe
from frappe.model.document import Document

class Emergency(Document):
    def before_insert(self):
        if not self.receptionist:
            user_full_name = frappe.db.get_value("User", frappe.session.user, "full_name")
            self.receptionist = user_full_name

    def before_save(self):
      
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
                "emergency": self.emergency,
            	"address": self.address
            })
            new_patient.insert(ignore_permissions=True)

            # Assign the new patient_id to the appointment
            self.patient_id = new_patient.name
            frappe.msgprint(f"New patient created: {new_patient.name}", alert=True)