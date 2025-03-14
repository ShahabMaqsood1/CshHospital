// Copyright (c) 2025, Shahab Maqsood and contributors
// For license information, please see license.txt

frappe.query_reports["Lab Reports"] = {
	"filters": [
		{
            "fieldname": "from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            "reqd": 1
        },
        {
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            "reqd": 1
        },
        {
            "fieldname": "patient_id",
            "label": __("Medical Record Number (MR)"),
            "fieldtype": "Data",
            "reqd": 0
        },
        {
            "fieldname": "patient_name",
            "label": __("Patient Name"),
            "fieldtype": "Data",
            "reqd": 0
        },
        {
            "fieldname": "lab_tests",
            "label": __("Lab Test"),
            "fieldtype": "Data",
            "reqd": 0
        },
        {
            "fieldname": "receptionist",
            "label": __("Receptionist"),
            "fieldtype": "Data",
            "reqd": 0
        }
	]
};
