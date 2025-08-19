import frappe

def execute(filters=None):
    if not filters.get('from_date') or not filters.get('to_date'):
        frappe.throw("Please select both From Date and To Date")

    # Define columns
    columns = [

        {"label": "Admission Number", "fieldname": "admission_no", "fieldtype": "data", "width": 120},
        {"label": "MR#", "fieldname": "patient_id", "fieldtype": "data", "width": 120},
        {"label": "date_of_admission", "fieldname": "date_of_admission", "fieldtype": "date", "width": 120},
	
        {"label": "date_of_discharge", "fieldname": "date_of_discharge", "fieldtype": "date", "width": 120},
        {"label": "time_of_admission", "fieldname": "time_of_admission", "fieldtype": "time", "width": 120},
        {"label": "time_of_discharge", "fieldname": "time_of_discharge", "fieldtype": "time", "width": 120},
	
        {"label": "no_of_days", "fieldname": "no_of_days", "fieldtype": "int", "width": 120},
        {"label": "admit_in", "fieldname": "admit_in", "fieldtype": "data", "width": 120},
        {"label": "patient_name", "fieldname": "patient_name", "fieldtype": "data", "width": 120},
	
        {"label": "on_oxygen_days", "fieldname": "on_oxygen_days", "fieldtype": "data", "width": 120},
        {"label": "admission_fee", "fieldname": "admission_fee", "fieldtype": "data", "width": 120},
        {"label": "operation_fee", "fieldname": "operation_fee", "fieldtype": "data", "width": 120},
	
        {"label": "anaethetist_fee", "fieldname": "anaethetist_fee", "fieldtype": "data", "width": 120},
        {"label": "theater_charges", "fieldname": "theater_charges", "fieldtype": "data", "width": 120},
        {"label": "tahir_visiting_fee", "fieldname": "tahir_visiting_fee", "fieldtype": "data", "width": 120},
	{"label": "abdul_visiting_fee", "fieldname": "abdul_visiting_fee", "fieldtype": "data", "width": 120},
	{"label": "abid_visiting_fee", "fieldname": "abid_visiting_fee", "fieldtype": "data", "width": 120},
      {"label": "Dr Moeeza Visiting Fee", "fieldname": "dr_moeeza", "fieldtype": "data", "width": 120},
	{"label": "medical_officer", "fieldname": "medical_officer", "fieldtype": "data", "width": 120},
	{"label": "ward_charges", "fieldname": "ward_charges", "fieldtype": "data", "width": 120},
	{"label": "icu_charges", "fieldname": "icu_charges", "fieldtype": "data", "width": 120},
	
	{"label": "room_charges", "fieldname": "room_charges", "fieldtype": "data", "width": 120},
	{"label": "oxygen_charges", "fieldname": "oxygen_charges", "fieldtype": "data", "width": 120},
	{"label": "nursing_care", "fieldname": "nursing_care", "fieldtype": "data", "width": 120},
	{"label": "circumcision_charges", "fieldname": "circumcision_charges", "fieldtype": "data", "width": 120},
	{"label": "medicine_charges", "fieldname": "medicine_charges", "fieldtype": "data", "width": 120},
	{"label": "monitoring_charges", "fieldname": "monitoring_charges", "fieldtype": "data", "width": 120},
	{"label": "ota_charges", "fieldname": "ota_charges", "fieldtype": "data", "width": 120},
	{"label": "total", "fieldname": "total", "fieldtype": "data", "width": 120},
	{"label": "advance", "fieldname": "advance", "fieldtype": "data", "width": 120},
{"label": "discount", "fieldname": "discount", "fieldtype": "data", "width": 120},
{"label": "grand_total", "fieldname": "grand_total", "fieldtype": "data", "width": 120},

    ]

    # Base SQL query
    base_query = """
        SELECT  
            na.admission_no AS admission_no,
	    na.patient_id AS patient_id,
	    na.date_of_admission AS date_of_admission,
	    na.date_of_discharge AS date_of_discharge,
            na.time_of_admission AS time_of_admission,
	    na.time_of_discharge AS time_of_discharge,
	    na.no_of_days AS no_of_days,
	    na.admit_in AS admit_in,
	    na.patient_name AS patient_name,
	    na.on_oxygen_days AS on_oxygen_days,
	    na.admission_fee AS admission_fee,
	    na.operation_fee AS operation_fee,
	    na.anaethetist_fee AS anaethetist_fee,
	    na.theater_charges AS theater_charges,
	    na.tahir_visiting_fee AS tahir_visiting_fee,
        na.dr_moeeza AS dr_moeeza,
	    na.abdul_visiting_fee AS abdul_visiting_fee,
	    na.abid_visiting_fee AS abid_visiting_fee,
	    na.medical_officer AS medical_officer,
	    na.ward_charges AS ward_charges,
	    na.icu_charges AS icu_charges,
	    na.room_charges AS room_charges,
	    na.oxygen_charges AS oxygen_charges,
	    na.nursing_care AS nursing_care,
	    na.circumcision_charges AS circumcision_charges,
	    na.medicine_charges AS medicine_charges,
	    na.monitoring_charges AS monitoring_charges,
	    na.ota_charges AS ota_charges,
	    na.total AS total,
	    na.advance AS advance,
	    na.discount AS discount,
	    na.grand_total AS grand_total
        FROM 
            `tabDischarge Bill` na

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


    # Add time filter
    if filters.get('from_time') and filters.get('to_time'):
        conditions += " AND na.time_of_discharge BETWEEN %s AND %s"
        values.append(filters.get('from_time'))
        values.append(filters.get('to_time'))

    # Complete query with conditions
    query = base_query + conditions + """
        ORDER BY 
            na.date, na.time_of_discharge
    """

    # Execute the query
    raw_data = frappe.db.sql(query, values, as_dict=True)

    # Prepare the data to return
    return columns, raw_data
