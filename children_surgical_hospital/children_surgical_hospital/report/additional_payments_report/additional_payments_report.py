import frappe

def execute(filters=None):
    if not filters.get('from_date') or not filters.get('to_date'):
        return [], []  # Return empty if filters are missing

    # Define columns
    columns = [
        {"label": "Medical Record Number (MR)", "fieldname": "patient_id", "fieldtype": "Data", "width": 120},
        {"label": "Patient Name", "fieldname": "patient_name", "fieldtype": "Data", "width": 120},
        {"label": "Father Name", "fieldname": "father_name", "fieldtype": "Data", "width": 120},
        {"label": "Gender", "fieldname": "gender", "fieldtype": "Data", "width": 120},
        {"label": "Age", "fieldname": "age", "fieldtype": "Data", "width": 100},
        {"label": "Weight", "fieldname": "weight", "fieldtype": "Data", "width": 100},
        {"label": "Phone No", "fieldname": "phone_number", "fieldtype": "Data", "width": 100},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 120},
        {"label": "CNIC", "fieldname": "cnic", "fieldtype": "Data", "width": 120},
        {"label": "Email", "fieldname": "email", "fieldtype": "Data", "width": 120},
        {"label": "Payment For", "fieldname": "payment", "fieldtype": "Select", "width": 100},
        {"label": "Duration", "fieldname": "duration", "fieldtype": "Select", "width": 100},
        {"label": "Payment Amount", "fieldname": "payment_amount", "fieldtype": "Currency", "width": 100},
        {"label": "Date", "fieldname": "date", "fieldtype": "Date", "width": 100},
        {"label": "Time", "fieldname": "time", "fieldtype": "Time", "width": 100},
        {"label": "Receptionist", "fieldname": "receptionist", "fieldtype": "Data", "width": 100},
    ]

    # Base SQL query
    query = """
        SELECT 
            ap.patient_id AS patient_id,
            ap.patient_name AS patient_name,
            ap.father_name AS father_name,
            ap.gender AS gender,
            ap.age AS age,
            ap.weight AS weight,
            ap.phone_number AS phone_number,
            ap.cnic AS cnic,
            ap.email AS email,
            ap.payment AS payment,
            ap.duration AS duration,
            ap.payment_amount AS payment_amount,
            ap.date AS date,
            ap.time AS time,
            ap.receptionist AS receptionist
        FROM 
            `tabAdditional Payments` ap
        WHERE 
            ap.docstatus IN (0, 1)
            AND ap.date BETWEEN %(from_date)s AND %(to_date)s
    """

    # Add time filter if provided
    if filters.get("from_time") and filters.get("to_time"):
        query += " AND ap.time BETWEEN %(from_time)s AND %(to_time)s"

    # Execute the query
    data = frappe.db.sql(query, filters, as_dict=True)

    return columns, data
