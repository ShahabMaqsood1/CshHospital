import frappe

def execute(filters=None):
    if not filters.get('from_date') or not filters.get('to_date'):
        frappe.throw("Please select both From Date and To Date")

    # Define columns
    columns = [
        {"label": "Medical Record Number (MR)", "fieldname": "patient_id", "fieldtype": "Data", "width": 150},
        {"label": "Patient Name", "fieldname": "patient_name", "fieldtype": "Data", "width": 200},
        {"label": "Doctor", "fieldname": "dr_id", "fieldtype": "Data", "width": 150},
        {"label": "Operation", "fieldname": "operations", "fieldtype": "Data", "width": 200},
        {"label": "Operation Doctor ID", "fieldname": "operation_doctor_id", "fieldtype": "Data", "width": 150},
        {"label": "Anesthesia Doctor", "fieldname": "anesthesia_doctor", "fieldtype": "Data", "width": 150},
        {"label": "Payment Date", "fieldname": "payment_date", "fieldtype": "Date", "width": 120},
	{"label": "Total Payment", "fieldname": "total_payment_amount", "fieldtype": "Date", "width": 120},
        {"label": "Amount Paid", "fieldname": "payment_amount", "fieldtype": "Currency", "width": 120},
        {"label": "Due Amount", "fieldname": "payment_remarks", "fieldtype": "Data", "width": 250},
        {"label": "Date of Admission", "fieldname": "date", "fieldtype": "Date", "width": 120},
        {"label": "Time", "fieldname": "time_of_admission", "fieldtype": "Time", "width": 120},
        {"label": "Date of Discharge", "fieldname": "date_of_discharge", "fieldtype": "Date", "width": 120},
        {"label": "Time of Discharge", "fieldname": "time_of_discharge", "fieldtype": "Time", "width": 120},
    ]

    # Base SQL query
    base_query = """
        SELECT  
            na.patient_id AS patient_id,
            na.patient_name AS patient_name,
            na.dr_id AS dr_id,
            nao.operations AS operations,
            nao.operation_doctor_id AS operation_doctor_id,
            nao.anesthesia_doctor AS anesthesia_doctor,
            nap.date AS payment_date,
            nap.payment_amount AS payment_amount,
	    nap.total_payment_amount AS total_payment_amount,
            nap.remarks AS payment_remarks,
            na.date AS date,
            na.time_of_admission AS time_of_admission,
            na.date_of_discharge AS date_of_discharge,
            na.time_of_discharge AS time_of_discharge
        FROM 
            `tabNew Admission` na
        LEFT JOIN 
            `tabAdmission Operations` nao ON nao.parent = na.name
        LEFT JOIN 
            `tabAdmission Payments` nap ON nap.parent = na.name
        WHERE 
            na.docstatus IN (0, 1)
            AND na.date BETWEEN %s AND %s
    """

    # Prepare conditions and values
    conditions = ""
    values = [filters.get('from_date'), filters.get('to_date')]

    # Add filter for Patient ID if provided
    if filters.get('patient_id'):
        conditions += " AND na.patient_id = %s"
        values.append(filters.get('patient_id'))

    # Add filter for Patient Name if provided
    if filters.get('patient_name'):
        conditions += " AND na.patient_name = %s"
        values.append(filters.get('patient_name'))

    # Add filter for Doctor ID if provided
    if filters.get('dr_id'):
        conditions += " AND na.dr_id = %s"
        values.append(filters.get('dr_id'))

    # Add filter for Operation if provided
    if filters.get('operations'):
        conditions += " AND nao.operations = %s"
        values.append(filters.get('operations'))

    # Complete query with conditions
    query = base_query + conditions + """
        ORDER BY 
            na.date, na.patient_name
    """

    # Execute the query
    raw_data = frappe.db.sql(query, values, as_dict=True)

    # Prepare the data to return
    return columns, raw_data
