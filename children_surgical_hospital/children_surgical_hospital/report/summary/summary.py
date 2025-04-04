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

    time_filter = ""
    time_params = []

    if filters.get('from_time') and filters.get('to_time'):
        time_filter = "AND TIME(creation) BETWEEN %s AND %s"
        time_params = [filters.get('from_time'), filters.get('to_time')]

    def fetch_and_append(query, params, category_name):
        data = frappe.db.sql(query, params, as_dict=True)
        if data and data[0]:
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

    revenue_categories = [
        ("Emergency Cases", f"""
            SELECT COUNT(*) AS total_count, COALESCE(SUM(ap.payment), 0) AS total_amount
            FROM `tabEmergency` na
            LEFT JOIN `tabEmergency Payment` ap ON na.name = ap.parent
            WHERE na.docstatus IN (0, 1) 
                AND na.date BETWEEN %s AND %s {receptionist_filter} {time_filter}
        """),
        ("Patient Appointments", f"""
            SELECT COUNT(*) AS total_count, COALESCE(SUM(remaining_total), 0) AS total_amount
            FROM `tabPatient Appointment`
            WHERE docstatus IN (0, 1) 
                AND appointment_date BETWEEN %s AND %s {receptionist_filter} {time_filter}
        """),
        ("New Admissions", f"""
            SELECT COUNT(*) AS total_count, COALESCE(SUM(ap.payment_amount), 0) AS total_amount
            FROM `tabNew Admission` na
            LEFT JOIN `tabAdmission Payments` ap ON na.name = ap.parent
            WHERE na.docstatus IN (0, 1) 
                AND na.date BETWEEN %s AND %s {receptionist_filter} {time_filter}
        """),
        ("Discharge Bill", f"""
            SELECT COUNT(*) AS total_count, COALESCE(SUM(grand_total), 0) AS total_amount
            FROM `tabDischarge Bill`
            WHERE docstatus IN (0, 1)
                AND date BETWEEN %s AND %s {receptionist_filter} {time_filter}
        """),
        ("Additional Payments", f"""
            SELECT COUNT(*) AS total_count, COALESCE(SUM(payment_amount), 0) AS total_amount
            FROM `tabAdditional Payments`
            WHERE docstatus IN (0, 1) 
                AND date BETWEEN %s AND %s {receptionist_filter} {time_filter}
        """),
        ("Lab Reports", f"""
            SELECT COUNT(DISTINCT parent) AS total_count, COALESCE(SUM(payment_amount), 0) AS total_amount
            FROM `tablab tests`
            WHERE parenttype = 'Lab Reports' 
                AND docstatus IN (0, 1) 
                AND parent IN (
                    SELECT name FROM `tabLab Reports` 
                    WHERE docstatus IN (0, 1) 
                        AND date_of_report BETWEEN %s AND %s {receptionist_filter} {time_filter}
                )
        """),
    ]

    total_income = 0

    for category, query in revenue_categories:
        fetch_and_append(query.format(receptionist_filter=receptionist_filter, time_filter=time_filter), 
                         (filters.get('from_date'), filters.get('to_date'), *receptionist_param, *time_params), category)
        total_income += report_data[-1]["total_amount"]

    report_data.append({
        "category": "<b>Total Income</b>",
        "total_count": "",
        "total_amount": total_income
    })

    expenses_query = f"""
        SELECT COUNT(*) AS total_count, COALESCE(SUM(payment_amount), 0) AS total_amount
        FROM `tabExpenses`
        WHERE docstatus IN (0, 1) 
            AND date BETWEEN %s AND %s {receptionist_filter} {time_filter}
    """
    fetch_and_append(expenses_query.format(receptionist_filter=receptionist_filter, time_filter=time_filter), 
                     (filters.get('from_date'), filters.get('to_date'), *receptionist_param, *time_params), "Expenses")

    total_expenses = report_data[-1]["total_amount"]
    net_total = total_income - total_expenses

    report_data.append({
        "category": "<b>Net Total</b>",
        "total_count": "",
        "total_amount": net_total
    })

    return columns, report_data
