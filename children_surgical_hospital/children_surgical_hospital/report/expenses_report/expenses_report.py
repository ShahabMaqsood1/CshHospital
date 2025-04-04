import frappe

def execute(filters=None):
    if not filters.get('from_date') or not filters.get('to_date'):
        frappe.throw("Please select both From Date and To Date")

    # Define columns
    columns = [
        {"label": "Name", "fieldname": "name1", "fieldtype": "Data", "width": 150},
        {"label": "Reason for Payment", "fieldname": "reason_for_payment", "fieldtype": "Data", "width": 200},
        {"label": "Payment Amount", "fieldname": "payment_amount", "fieldtype": "Currency", "width": 150},
        {"label": "Date", "fieldname": "date", "fieldtype": "Date", "width": 120},
        {"label": "Time", "fieldname": "time", "fieldtype": "Time", "width": 120},
        {"label": "Receptionist", "fieldname": "receptionist", "fieldtype": "Data", "width": 150}
    ]

    # Base SQL query
    query = """
        SELECT 
            ex.name1 AS name1,
            ex.reason_for_payment AS reason_for_payment,
            ex.payment_amount AS payment_amount,
            ex.date AS date,
            ex.time AS time,
            ex.receptionist AS receptionist
        FROM 
            `tabExpenses` ex
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
    if filters.get("name"):
        query += " AND ex.name = %s"
        values.append(filters.get("name"))

    # Complete query with ordering
    query += " ORDER BY ex.date, ex.time"

    # Execute query
    raw_data = frappe.db.sql(query, values, as_dict=True)

    return columns, raw_data
