// Copyright (c) 2025, Shahab Maqsood and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Quick Entry", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on('Quick Entry', {
    select_doctype: function(frm) {
        if (frm.doc.select_doctype) {
            frappe.new_doc(frm.doc.select_doctype);
        }
    },
    select_report: function(frm) {
        if (frm.doc.select_report) {
            let report_name = encodeURIComponent(frm.doc.select_report); // Ensure proper URL formatting
            let url = `/app/query-report/${report_name}`;
            window.location.href = url;  // Redirect to the report page
        }
    }
});
