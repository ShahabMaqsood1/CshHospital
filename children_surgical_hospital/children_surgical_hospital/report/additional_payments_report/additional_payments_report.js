// Copyright (c) 2025, Shahab Maqsood and contributors
// For license information, please see license.txt

frappe.query_reports["Additional Payments report"] = {
	"filters": [
		{
            "fieldname": "from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.add_days(frappe.datetime.get_today(), -7),
            "reqd": 1
        },
        {
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.get_today(),
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
        }
	]
};
