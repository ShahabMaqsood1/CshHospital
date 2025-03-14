import frappe

def execute(filters=None):
    if filters.get('from_date') and filters.get('to_date'):
        # Define columns
        columns = [
            {"label": "Naming Series", "fieldname": "naming_series", "fieldtype": "Data", "width": 150},
            {"label": "Medical Record Number (MR)", "fieldname": "patient_id", "fieldtype": "Data", "width": 120},
            {"label": "Patient Name", "fieldname": "patient_name", "fieldtype": "Data", "width": 200},
            {"label": "Doctor ID", "fieldname": "doctor_id", "fieldtype": "Data", "width": 200},
            {"label": "Age", "fieldname": "age", "fieldtype": "Data", "width": 100},
            {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 120},
            {"label": "NVF", "fieldname": "nvf", "fieldtype": "Check", "width": 80},
            {"label": "Original Charge", "fieldname": "payment", "fieldtype": "Currency", "width": 200},
            {"label": "Discount", "fieldname": "discount", "fieldtype": "Currency", "width": 200},
            {"label": "Remaining Total", "fieldname": "remaining_total", "fieldtype": "Currency", "width": 200},
            {"label": "Appointment Date", "fieldname": "appointment_date", "fieldtype": "Date", "width": 150},
            {"label": "Appointment Time", "fieldname": "appointment_time", "fieldtype": "Time", "width": 150},
            {"label": "Receptionist", "fieldname": "receptionist", "fieldtype": "Data", "width": 200},
        ]

        # Base SQL query
        base_query = """
            SELECT 
                pa.naming_series AS naming_series,
                pa.patient_id AS patient_id,
                pa.patient_name AS patient_name,
                pa.doctor_id AS doctor_id,
                pa.age AS age,
                pa.status AS status,
                pa.nvf AS nvf,
                pa.payment AS payment,
                pa.discount AS discount,
                pa.remaining_total AS remaining_total,
                pa.appointment_date AS appointment_date,
                pa.appointment_time AS appointment_time,
                pa.receptionist AS receptionist
            FROM 
                `tabPatient Appointment` pa
            WHERE 
                pa.docstatus IN (0, 1)
                AND pa.appointment_date BETWEEN %s AND %s
        """

        # Prepare conditions and values
        conditions = ""
        values = [filters.get('from_date'), filters.get('to_date')]

        # Add filter for Patient ID if provided
        if filters.get('patient_id'):
            conditions += " AND pa.patient_id = %s"
            values.append(filters.get('patient_id'))

        # Add filter for Doctor ID if provided
        if filters.get('doctor_id'):
            conditions += " AND pa.doctor_id = %s"
            values.append(filters.get('doctor_id'))

        # Complete query with conditions
        query = base_query + conditions + " ORDER BY pa.appointment_date, pa.appointment_time"

        # Execute the query
        raw_data = frappe.db.sql(query, values, as_dict=True)

        # Return data
        return columns, raw_data
    else:
        return [], []
