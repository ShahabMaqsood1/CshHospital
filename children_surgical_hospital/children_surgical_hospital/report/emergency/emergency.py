import frappe

def execute(filters=None):
    if not filters.get('from_date') or not filters.get('to_date'):
        frappe.throw("Please select both From Date and To Date")

    # Define base columns
    columns = [
        {"label": "Date", "fieldname": "date", "fieldtype": "Date", "width": 120},
        {"label": "Time", "fieldname": "time", "fieldtype": "Time", "width": 120},
        {"label": "MR#", "fieldname": "patient_id", "fieldtype": "Data", "width": 150},
        {"label": "Patient Name", "fieldname": "patient_name", "fieldtype": "Data", "width": 200},
        {"label": "Gender", "fieldname": "gender", "fieldtype": "Data", "width": 100},
        {"label": "Father Name", "fieldname": "father_name", "fieldtype": "Data", "width": 200},
        {"label": "Address", "fieldname": "address", "fieldtype": "Data", "width": 250},
        {"label": "Phone", "fieldname": "phone_number", "fieldtype": "Data", "width": 150},
        {"label": "Initial Diagnose", "fieldname": "initial_diagnose", "fieldtype": "Data", "width": 250},
        {"label": "Doctor", "fieldname": "doctor", "fieldtype": "Link", "options": "Doctor", "width": 150},
        {"label": "Disposal", "fieldname": "disposal", "fieldtype": "Data", "width": 150},
        {"label": "Receptionist", "fieldname": "receptionist", "fieldtype": "Data", "width": 150},
        {"label": "Signature", "fieldname": "signature", "fieldtype": "Data", "width": 150},
    ]

    # Add the Fee column if 'show_fee' is checked
    if filters.get("show_fee"):
        columns.insert(10, {"label": "Fee", "fieldname": "fee", "fieldtype": "Currency", "width": 150})

    # Base SQL query
    base_query = """
        SELECT 
            e.date, e.time, e.patient_id, e.patient_name, e.gender, e.father_name, e.address, e.phone_number, 
            e.initial_diagnose, e.doctor, e.disposal, e.receptionist, e.signature
    """

    # Append fee field conditionally
    if filters.get("show_fee"):
        base_query += ", (SELECT COALESCE(SUM(payment), 0) FROM `tabEmergency Payment` ep WHERE ep.parent = e.name) AS fee"

    base_query += " FROM `tabEmergency` e WHERE e.docstatus IN (0, 1) AND e.date BETWEEN %s AND %s"

    # Prepare query values
    values = [filters.get('from_date'), filters.get('to_date')]

    # Add optional time filter
    if filters.get("from_time"):
        base_query += " AND e.time >= %s"
        values.append(filters.get("from_time"))

    if filters.get("to_time"):
        base_query += " AND e.time <= %s"
        values.append(filters.get("to_time"))

    # Add optional patient_id filter
    if filters.get("patient_id"):
        base_query += " AND e.patient_id = %s"
        values.append(filters.get("patient_id"))

    # Add optional doctor filter
    if filters.get("doctor"):
        base_query += " AND e.doctor = %s"
        values.append(filters.get("doctor"))

    # Complete query with ordering
    base_query += " ORDER BY e.date, e.time"

    # Execute the query
    raw_data = frappe.db.sql(base_query, values, as_dict=True)

    return columns, raw_data
