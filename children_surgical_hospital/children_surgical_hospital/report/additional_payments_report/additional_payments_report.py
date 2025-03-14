import frappe

def execute(filters=None):
    if not filters.get('from_date') or not filters.get('to_date'):
        return [], []  # Return empty if filters are missing

    # Define columns
    columns = [
        {"label": "Payment For", "fieldname": "payment", "fieldtype": "Data", "width": 150},
        {"label": "Medical Record Number (MR)", "fieldname": "patient_id", "fieldtype": "Data", "width": 120},
        {"label": "Patient Name", "fieldname": "patient_name", "fieldtype": "Data", "width": 200},
        {"label": "Age", "fieldname": "age", "fieldtype": "Int", "width": 100},
        {"label": "Reason", "fieldname": "reason", "fieldtype": "Data", "width": 200},
        {"label": "Payment Amount", "fieldname": "payment_amount", "fieldtype": "Currency", "width": 150},
        {"label": "Date", "fieldname": "date", "fieldtype": "Date", "width": 120},
        {"label": "Receptionist", "fieldname": "receptionist", "fieldtype": "Data", "width": 150},
    ]

    # Base SQL query
    query = """
        SELECT 
            ap.payment AS payment,
            ap.patient_id AS patient_id,
            ap.patient_name AS patient_name,
            ap.age AS age,
            ap.reason AS reason,
            ap.payment_amount AS payment_amount,
            ap.date AS date,
            ap.receptionist AS receptionist
        FROM 
            `tabAdditional Payments` ap
        WHERE 
            ap.docstatus IN (0, 1)
            AND ap.date BETWEEN %(from_date)s AND %(to_date)s
    """

    # Execute the query
    data = frappe.db.sql(query, filters, as_dict=True)

    return columns, data
