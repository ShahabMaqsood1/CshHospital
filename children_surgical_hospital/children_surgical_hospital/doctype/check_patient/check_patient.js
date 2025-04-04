// Copyright (c) 2024, Shahab Maqsood and contributors
// For license information, please see license.txt

frappe.ui.form.on('Check Patient', {
    setup: function(frm) {
        frm.set_query("appointment_no", function() {
            return {
                filters: {
                    docstatus: 0  // Show only Draft (unsaved/submittable) appointments
                }
            };
        });
    },

    discount: function(frm) {
        if (frm.doc.payment && frm.doc.discount) {
            let remaining_total = frm.doc.payment - frm.doc.discount;
            frm.set_value('remaining_total', remaining_total);

            if (frm.doc.appointment_no) {
                frappe.call({
                    method: 'frappe.client.get',
                    args: {
                        doctype: 'Patient Appointment',
                        name: frm.doc.appointment_no
                    },
                    callback: function(r) {
                        if (r.message) {
                            let appointment = r.message;
                            appointment.discount = frm.doc.discount;
                            appointment.remaining_total = remaining_total;

                            frappe.call({
                                method: 'frappe.client.save',
                                args: { doc: appointment },
                                callback: function(save_res) {
                                    if (save_res.message) {
                                        frappe.show_alert({
                                            message: __('Patient Appointment updated successfully'),
                                            indicator: 'green'
                                        });
                                    }
                                },
                                error: function(err) {
                                    frappe.msgprint(__('Failed to update Patient Appointment'));
                                }
                            });
                        } else {
                            frappe.msgprint(__('Patient Appointment not found'));
                        }
                    },
                    error: function(err) {
                        frappe.msgprint(__('Failed to fetch Patient Appointment'));
                    }
                });
            }
        }
    },
    
    payment: function(frm) {
        if (frm.doc.discount) {
            frm.trigger('discount');
        }
    },

    onload: function(frm) {  // Changed from 'refresh' to 'onload'
        ensure_new_row(frm, "report", "Presenting Complaints Table", "presenting_complaints");
        ensure_new_row(frm, "report1", "Medical Examination Findings Table", "medical_examination_findings");
        ensure_new_row(frm, "report2", "Patient Report", "prescription");
        ensure_new_row(frm, "lab_tests", "Lab Tests", "lab_tests");
    }
});

// Child Table Event Handlers
frappe.ui.form.on('Presenting Complaints Table', {
    presenting_complaints: function(frm, cdt, cdn) {
        ensure_new_row(frm, "report", "Presenting Complaints Table", "presenting_complaints");
    }
});

frappe.ui.form.on('Medical Examination Findings Table', {
    medical_examination_findings: function(frm, cdt, cdn) {
        ensure_new_row(frm, "report1", "Medical Examination Findings Table", "medical_examination_findings");
    }
});

frappe.ui.form.on('Patient Report', {
    prescription: function(frm, cdt, cdn) {
        ensure_new_row(frm, "report2", "Patient Report", "prescription");
    }
});

frappe.ui.form.on('Lab Tests', {
    lab_tests: function(frm, cdt, cdn) {
        ensure_new_row(frm, "lab_tests", "Lab Tests", "lab_tests");
    }
});

// Improved ensure_new_row() Function
function ensure_new_row(frm, parent_fieldname, child_doctype, trigger_field) {
    let child_table = frm.doc[parent_fieldname] || [];

    if (child_table.length === 0) {
        frm.add_child(parent_fieldname);
    } else {
        let last_row = child_table[child_table.length - 1];

        // Add a new row only if the last row has data AND required fields are filled
        if (last_row && last_row[trigger_field] && last_row.idx) {
            frm.add_child(parent_fieldname);
        }
    }

    frm.refresh_field(parent_fieldname);
} 
