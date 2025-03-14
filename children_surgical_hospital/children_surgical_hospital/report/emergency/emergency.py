import frappe

def execute(filters=None):
    if filters.get('from_date') and filters.get('to_date'):
        # Define base columns
        columns = [
            {"label": "Date", "fieldname": "date", "fieldtype": "Date", "width": 120},
            {"label": "Time", "fieldname": "time", "fieldtype": "Time", "width": 120},
            {"label": "MR#", "fieldname": "patient_id", "fieldtype": "Data", "width": 150},
            {"label": "Patient Name", "fieldname": "patient_name", "fieldtype": "Data", "width": 200},
            {"label": "Gender", "fieldname": "gender", "fieldtype": "Data", "width": 100},
            {"label": "Father Name", "fieldname": "father_name", "fieldtype": "Data", "width": 200},
            {"label": "Address", "fieldname": "address", "fieldtype": "Data", "width": 250},
            {"label": "Phone", "fieldname": "phone", "fieldtype": "Data", "width": 150},
            {"label": "Initial Diagnose", "fieldname": "initial_diagnose", "fieldtype": "Data", "width": 250},
            {"label": "Doctor", "fieldname": "doctor", "fieldtype": "Link", "options": "Doctor", "width": 150},
            {"label": "Disposal", "fieldname": "disposal", "fieldtype": "Data", "width": 150},
            {"label": "Receptionist", "fieldname": "receptionist", "fieldtype": "Data", "width": 150},
            {"label": "Signature", "fieldname": "signature", "fieldtype": "Data", "width": 150},
        ]

        # Add the Fee column only if 'show_fee' is checked
        if filters.get("show_fee"):
            columns.insert(10, {"label": "Fee", "fieldname": "fee", "fieldtype": "Currency", "width": 150})

        # Base SQL query
        base_query = """
            SELECT 
                date, time, patient_id, patient_name, gender, father_name, address, phone, 
                initial_diagnose, doctor, disposal, receptionist, signature
        """

        # Append fee field conditionally
        if filters.get("show_fee"):
            base_query += ", fee"

        base_query += " FROM `tabEmergency` WHERE docstatus IN (0, 1) AND date BETWEEN %s AND %s"

        # Prepare query values
        values = [filters.get('from_date'), filters.get('to_date')]

        # Add optional patient_id filter
        if filters.get("patient_id"):
            base_query += " AND patient_id = %s"
            values.append(filters.get("patient_id"))

        # Add optional doctor filter
        if filters.get("doctor"):
            base_query += " AND doctor = %s"
            values.append(filters.get("doctor"))

        # Complete query with ordering
        base_query += " ORDER BY date, time"

        # Execute the query
        raw_data = frappe.db.sql(base_query, values, as_dict=True)

        return columns, raw_data
    else:
        return [], []