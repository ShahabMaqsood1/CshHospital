import frappe

def execute(filters=None):
    if not filters.get('from_date') or not filters.get('to_date'):
        frappe.throw("Please select both From Date and To Date")

    # Define columns
    columns = [
        {"label": "Date", "fieldname": "date", "fieldtype": "Date", "width": 120},
        {"label": "Time", "fieldname": "time", "fieldtype": "Time", "width": 120},
        {"label": "Transfer Mode", "fieldname": "transfer_mode", "fieldtype": "Select", "width": 120},
        {"label": "Transferred By", "fieldname": "transferred_by", "fieldtype": "Select", "width": 120},
        {"label": "Receptionist", "fieldname": "receptionist", "fieldtype": "Data", "width": 120},
        {"label": "Transaction ID", "fieldname": "transaction_id", "fieldtype": "Data", "width": 120},
	{"label": "Payment Amount", "fieldname": "payment_amount", "fieldtype": "Currency", "width": 120},
	{"label": "MR No", "fieldname": "patient_id", "fieldtype": "Data", "width": 120},
	{"label": "Patient Name", "fieldname": "patient_name", "fieldtype": "Data", "width": 120},
	{"label": "Remarks", "fieldname": "remarks", "fieldtype": "Data", "width": 120}
    ]

    # Base SQL query
    query = """
        SELECT 
            ex.date AS date,
            ex.time AS time,
            ex.transfer_mode AS transfer_mode,
            ex.transferred_by AS transferred_by,
            ex.receptionist AS receptionist,
            ex.transaction_id AS transaction_id,
	    ex.payment_amount AS payment_amount,
  	    ex.patient_id AS patient_id,
	    ex.patient_name AS patient_name,
	    ex.remarks AS remarks
        FROM 
            `tabBank Deposit` ex
        WHERE 
            ex.docstatus IN (0, 1)
            AND ex.date BETWEEN %s AND %s
    """

    # Prepare conditions and values
    values = [filters.get('from_date'), filters.get('to_date')]

    # Apply optional time filter
    if filters.get("from_time"):
        query += " AND ex.time >= %s"
        values.append(filters.get("from_time"))

    if filters.get("to_time"):
        query += " AND ex.time <= %s"
        values.append(filters.get("to_time"))

    # Apply optional name filter
    

    # Complete query with ordering
    query += " ORDER BY ex.date, ex.time"

    # Execute query
    raw_data = frappe.db.sql(query, values, as_dict=True)

    return columns, raw_data
