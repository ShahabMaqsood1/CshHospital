// Copyright (c) 2025, Shahab Maqsood and contributors
// For license information, please see license.txt

frappe.query_reports["Emergency"] = {
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
        },
        {
            "fieldname": "patient_id",
            "label": __("MR#"),
            "fieldtype": "Data",
            "reqd": 0
        },
        {
            "fieldname": "doctor",
            "label": __("Doctor"),
            "fieldtype": "Link",
            "options": "Doctor",
            "reqd": 0
        },
        {
            "fieldname": "show_fee",
            "label": __("Show Fee"),
            "fieldtype": "Check",
            "default": 1
        }
    ]
};
