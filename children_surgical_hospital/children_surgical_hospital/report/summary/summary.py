import frappe

def execute(filters=None):
    if not filters or not filters.get('from_date') or not filters.get('to_date'):
        raise Exception("Please select both From Date and To Date")

    columns = [
        {"label": "Category", "fieldname": "category", "fieldtype": "Data", "width": 200},
        {"label": "Total Count", "fieldname": "total_count", "fieldtype": "Int", "width": 150},
        {"label": "Total Amount", "fieldname": "total_amount", "fieldtype": "Currency", "width": 200},
    ]

    report_data = []
    receptionist_filter = ""
    receptionist_param = []

    if filters.get('receptionist'):
        receptionist_filter = "AND receptionist = %s"
        receptionist_param = [filters.get('receptionist')]

    # Function to fetch and append data safely
    def fetch_and_append(query, params, category_name):
        data = frappe.db.sql(query, params, as_dict=True)
        if data and data[0]:  # Ensure the query returns valid data
            report_data.append({
                "category": category_name,
                "total_count": data[0].get("total_count", 0) or 0,
                "total_amount": data[0].get("total_amount", 0) or 0
            })
        else:
            report_data.append({
                "category": category_name,
                "total_count": 0,
                "total_amount": 0
            })

    # List of revenue categories
    revenue_categories = [
        ("Emergency Cases", """
            SELECT COUNT(*) AS total_count, COALESCE(SUM(ap.payment), 0) AS total_amount
            FROM `tabEmergency` na
            LEFT JOIN `tabEmergency Payment` ap ON na.name = ap.parent
            WHERE na.docstatus IN (0, 1) AND na.date BETWEEN %s AND %s {receptionist_filter}
        """),
        ("Patient Appointments", """
            SELECT COUNT(*) AS total_count, COALESCE(SUM(remaining_total), 0) AS total_amount
            FROM `tabPatient Appointment`
            WHERE docstatus IN (0, 1) AND appointment_date BETWEEN %s AND %s {receptionist_filter}
        """),
        ("New Admissions", """
            SELECT COUNT(*) AS total_count, COALESCE(SUM(ap.payment_amount), 0) AS total_amount
            FROM `tabNew Admission` na
            LEFT JOIN `tabAdmission Payments` ap ON na.name = ap.parent
            WHERE na.docstatus IN (0, 1) AND na.date BETWEEN %s AND %s {receptionist_filter}
        """),
        ("Additional Payments", """
            SELECT COUNT(*) AS total_count, COALESCE(SUM(payment_amount), 0) AS total_amount
            FROM `tabAdditional Payments`
            WHERE docstatus IN (0, 1) AND date BETWEEN %s AND %s {receptionist_filter}
        """),
        ("Lab Reports", """
            SELECT COUNT(DISTINCT parent) AS total_count, COALESCE(SUM(payment_amount), 0) AS total_amount
            FROM `tablab tests`
            WHERE parenttype = 'Lab Reports' AND docstatus IN (0, 1) AND parent IN (
                SELECT name FROM `tabLab Reports` 
                WHERE docstatus IN (0, 1) AND date_of_report BETWEEN %s AND %s {receptionist_filter}
            )
        """)
    ]

    total_income = 0

    for category, query in revenue_categories:
        fetch_and_append(query.format(receptionist_filter=receptionist_filter), 
                         (filters.get('from_date'), filters.get('to_date'), *receptionist_param), category)
        total_income += report_data[-1]["total_amount"]

    # Add Total Income
    report_data.append({
        "category": "<b>Total Income</b>",
        "total_count": "",
        "total_amount": total_income
    })

    # Expenses
    expenses_query = f"""
        SELECT COUNT(*) AS total_count, COALESCE(SUM(payment_amount), 0) AS total_amount
        FROM `tabExpenses`
        WHERE docstatus IN (0, 1) AND date BETWEEN %s AND %s {receptionist_filter}
    """
    fetch_and_append(expenses_query, (filters.get('from_date'), filters.get('to_date'), *receptionist_param), "Expenses")

    total_expenses = report_data[-1]["total_amount"]

    # Net Total (Total Income - Expenses)
    net_total = total_income - total_expenses

    report_data.append({
        "category": "<b>Net Total</b>",
        "total_count": "",
        "total_amount": net_total
    })

    # Debugging Output
    print("Generated Report Data:", report_data)

    return columns, report_data
