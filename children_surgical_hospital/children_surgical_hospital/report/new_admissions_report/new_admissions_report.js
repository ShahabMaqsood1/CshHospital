// Copyright (c) 2025, Shahab Maqsood and contributors
// For license information, please see license.txt

frappe.query_reports["New Admissions Report"] = {
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
            "fieldname": "dr_id",
            "label": __("Doctor ID"),
            "fieldtype": "Data",
            "reqd": 0
        },
        {
            "fieldname": "operations",
            "label": __("Operation"),
            "fieldtype": "Data",
            "reqd": 0
        },
        {
            "fieldname": "from_time",
            "label": __("From Time"),
            "fieldtype": "Time",
            "reqd": 0
        },
        {
            "fieldname": "to_time",
            "label": __("To Time"),
            "fieldtype": "Time",
            "reqd": 0
        }
	]
};
