// Copyright (c) 2025, Shahab Maqsood and contributors
// For license information, please see license.txt

frappe.query_reports["Summary Report"] = {
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
            "fieldname": "receptionist",
            "label": __("Receptionist"),
            "fieldtype": "Link",
            "options": "User",
            "default": "",
            "reqd": 0
        }
    ]
};
