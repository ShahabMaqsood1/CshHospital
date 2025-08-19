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
        ("Emergency Cases", "Emergency", """
            SELECT COUNT(*) AS total_count, COALESCE(SUM(ap.payment), 0) AS total_amount
            FROM `tabEmergency` na
            LEFT JOIN `tabEmergency Payment` ap ON na.name = ap.parent
            WHERE na.docstatus IN (0, 1)
                AND na.date BETWEEN %s AND %s {receptionist_filter} {time_filter}
        """),
        ("Patient Appointments", "Patient Appointment", """
            SELECT COUNT(*) AS total_count, COALESCE(SUM(remaining_total), 0) AS total_amount
            FROM `tabPatient Appointment`
            WHERE docstatus IN (0, 1)
                AND appointment_date BETWEEN %s AND %s {receptionist_filter} {time_filter}
        """),
        ("New Admissions", "New Admissions Report", """
            SELECT COUNT(*) AS total_count, COALESCE(SUM(ap.payment_amount), 0) AS total_amount
            FROM `tabNew Admission` na
            LEFT JOIN `tabAdmission Payments` ap ON na.name = ap.parent
            WHERE na.docstatus IN (0, 1)
                AND ap.date BETWEEN %s AND %s {receptionist_filter} {time_filter}
        """),
        ("Discharge Bill", "Discharge Report", """
            SELECT COUNT(*) AS total_count, COALESCE(SUM(grand_total), 0) AS total_amount
            FROM `tabDischarge Bill`
            WHERE docstatus IN (0, 1)
                AND date BETWEEN %s AND %s {receptionist_filter} {time_filter}
        """),
        ("Additional Payments", "Additional Payments Report", """
            SELECT COUNT(*) AS total_count, COALESCE(SUM(payment_amount), 0) AS total_amount
            FROM `tabAdditional Payments`
            WHERE docstatus IN (0, 1)
                AND date BETWEEN %s AND %s {receptionist_filter} {time_filter}
        """),
        ("Lab Reports", "Lab Reports", """
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
    detail_rows = []

    for category, report_name, raw_query in revenue_categories:
        query = raw_query.format(receptionist_filter=receptionist_filter, time_filter=time_filter)
        params = (filters.get('from_date'), filters.get('to_date'), *receptionist_param, *time_params)
        fetch_and_append(query, params, category)
        total_income += report_data[-1]["total_amount"]

        if filters.get("show_details"):
            detail = get_report_data(report_name, filters)
            if detail:
                detail_rows.append({"category": f"--- {category} Details ---"})
                detail_rows.extend(detail)

    report_data.append({
        "category": "<b>Total Income</b>",
        "total_count": "",
        "total_amount": total_income
    })

    # Bank Deposit from Admission Payments (online payments)
    bank_deposit_query = """
        SELECT COALESCE(SUM(ap.payment_amount), 0) AS total_amount
        FROM `tabNew Admission` na
        LEFT JOIN `tabAdmission Payments` ap ON na.name = ap.parent
        WHERE na.docstatus IN (0, 1)
            AND ap.date BETWEEN %s AND %s
            AND ap.payment_method = 'Bank Deposit'
            {receptionist_filter} {time_filter}
    """.format(receptionist_filter=receptionist_filter, time_filter=time_filter)

    bank_data = frappe.db.sql(
        bank_deposit_query,
        (filters.get('from_date'), filters.get('to_date'), *receptionist_param, *time_params),
        as_dict=True
    )
    bank_deposit_amount = bank_data[0]["total_amount"] if bank_data and bank_data[0] else 0

    # Bank Deposit (new doctype)
    bank_deposit_new_query = """
        SELECT COALESCE(SUM(payment_amount), 0) AS total_amount
        FROM `tabBank Deposit`
        WHERE docstatus IN (0, 1)
            AND date BETWEEN %s AND %s {receptionist_filter} {time_filter}
    """.format(receptionist_filter=receptionist_filter, time_filter=time_filter)

    bank_deposit_new_data = frappe.db.sql(
        bank_deposit_new_query,
        (filters.get('from_date'), filters.get('to_date'), *receptionist_param, *time_params),
        as_dict=True
    )
    bank_deposit_new_amount = bank_deposit_new_data[0]["total_amount"] if bank_deposit_new_data and bank_deposit_new_data[0] else 0

    report_data.append({
        "category": "Online Payments",
        "total_count": "",
        "total_amount": bank_deposit_amount
    })

    report_data.append({
        "category": "Bank Deposit",
        "total_count": "",
        "total_amount": bank_deposit_new_amount
    })

    cash_in_hand = total_income - bank_deposit_amount - bank_deposit_new_amount

    report_data.append({
        "category": "<b>Cash in Hand</b>",
        "total_count": "",
        "total_amount": cash_in_hand
    })

    # Expenses
    expenses_query = """
        SELECT COUNT(*) AS total_count, COALESCE(SUM(payment_amount), 0) AS total_amount
        FROM `tabExpenses`
        WHERE docstatus IN (0, 1)
            AND date BETWEEN %s AND %s {receptionist_filter} {time_filter}
    """.format(receptionist_filter=receptionist_filter, time_filter=time_filter)

    fetch_and_append(expenses_query,
                     (filters.get('from_date'), filters.get('to_date'), *receptionist_param, *time_params),
                     "Expenses")

    total_expenses = report_data[-1]["total_amount"]

    report_data.append({
        "category": "<b>Net Total</b>",
        "total_count": "",
        "total_amount": cash_in_hand - total_expenses
    })

    # Append detail rows if enabled
    if filters.get("show_details") and detail_rows:
        report_data.append({})
        report_data.extend(detail_rows)

    return columns, report_data


def get_report_data(report_name, filters):
    try:
        report = frappe.get_doc("Report", report_name)
        result = report.get_data(filters=filters)
        return result
    except Exception as e:
        frappe.log_error(f"Error fetching report {report_name}: {str(e)}")
        return []
