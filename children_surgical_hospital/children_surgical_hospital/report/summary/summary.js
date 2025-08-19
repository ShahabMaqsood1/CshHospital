frappe.query_reports["Summary Report"] = {
    filters: [
        {
            fieldname: "from_date",
            label: "From Date",
            fieldtype: "Date",
            reqd: 1,
            default: frappe.datetime.add_days(frappe.datetime.get_today(), -7)
        },
        {
            fieldname: "to_date",
            label: "To Date",
            fieldtype: "Date",
            reqd: 1,
            default: frappe.datetime.get_today()
        },
        {
            fieldname: "from_time",
            label: "From Time",
            fieldtype: "Time"
        },
        {
            fieldname: "to_time",
            label: "To Time",
            fieldtype: "Time"
        },
        {
            fieldname: "receptionist",
            label: "Receptionist",
            fieldtype: "Link",
            options: "User"
        },
        {
            fieldname: "show_details",
            label: "Show Detailed Entries",
            fieldtype: "Check",
            default: 0
        }
    ]
};
