import frappe

def execute(filters=None):
    if not filters.get('from_date') or not filters.get('to_date'):
        frappe.throw("Please select both From Date and To Date")

    # Define columns
    columns = [
        {"label": "Medical Record Number (MR)", "fieldname": "patient_id", "fieldtype": "Data", "width": 150},
        {"label": "Patient Name", "fieldname": "patient_name", "fieldtype": "Data", "width": 200},
        {"label": "Lab Test", "fieldname": "lab_tests", "fieldtype": "Data", "width": 200},
        {"label": "Results", "fieldname": "upload_results", "fieldtype": "Attach", "width": 150},
        {"label": "Payment Amount", "fieldname": "payment_amount", "fieldtype": "Currency", "width": 120},
        {"label": "Receptionist", "fieldname": "receptionist", "fieldtype": "Data", "width": 150},
        {"label": "Date of Report", "fieldname": "date_of_report", "fieldtype": "Date", "width": 120},
    ]

    # Base SQL query
    base_query = """
        SELECT  
            lr.patient_id AS patient_id,
            lr.patient_name AS patient_name,
            lri.lab_tests AS lab_tests,
            lri.upload_results AS upload_results,
            lri.payment_amount AS payment_amount,
            lr.receptionist AS receptionist,
            lr.date_of_report AS date_of_report
        FROM 
            `tabLab Reports` lr
        LEFT JOIN 
            `tablab tests` lri ON lri.parent = lr.name
        WHERE 
            lr.docstatus IN (0, 1)
            AND lr.date_of_report BETWEEN %s AND %s
    """

    # Prepare conditions and values
    conditions = ""
    values = [filters.get('from_date'), filters.get('to_date')]

    # Add filter for Patient ID if provided
    if filters.get('patient_id'):
        conditions += " AND lr.patient_id = %s"
        values.append(filters.get('patient_id'))

    # Add filter for Patient Name if provided
    if filters.get('patient_name'):
        conditions += " AND lr.patient_name = %s"
        values.append(filters.get('patient_name'))

    # Add filter for Lab Test if provided
    if filters.get('lab_tests'):
        conditions += " AND lri.lab_tests = %s"
        values.append(filters.get('lab_tests'))

    # Add filter for Receptionist if provided
    if filters.get('receptionist'):
        conditions += " AND lr.receptionist = %s"
        values.append(filters.get('receptionist'))

    # Complete query with conditions
    query = base_query + conditions + """
        ORDER BY 
            lr.date_of_report, lr.patient_name
    """

    # Execute the query
    raw_data = frappe.db.sql(query, values, as_dict=True)

    # Prepare the data to return
    return columns, raw_data
