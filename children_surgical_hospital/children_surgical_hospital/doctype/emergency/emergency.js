// Copyright (c) 2024, Shahab Maqsood and contributors
// For license information, please see license.txt
let phoneSearchTimeout;

frappe.ui.form.on("Emergency", {
    phone_number: function (frm) {
        if (phoneSearchTimeout) {
            clearTimeout(phoneSearchTimeout);
        }

        phoneSearchTimeout = setTimeout(() => {
            if (frm.doc.phone_number) {
                frappe.call({
                    method: "frappe.client.get_list",
                    args: {
                        doctype: "Patient Record",
                        filters: {
                            contact_number: frm.doc.phone_number
                        },
                        fields: ["name", "patient_name", "contact_number"]
                    },
                    callback: function (response) {
                        let patients = response.message;
                        if (patients.length > 0) {
                            let options = patients.map(patient => ({
                                label: `${patient.patient_name} (${patient.contact_number})`,
                                value: patient.name
                            }));

                            frappe.prompt(
                                [
                                    {
                                        label: "Select Patient",
                                        fieldname: "selected_patient",
                                        fieldtype: "Select",
                                        options: options.map(opt => opt.label)
                                    }
                                ],
                                (data) => {
                                    let selected = options.find(opt => opt.label === data.selected_patient);
                                    if (selected) {
                                        frm.set_value("patient_id", selected.value);
                                        frm.trigger("fetch_patient_data"); // Fetch data once selected
                                    }
                                },
                                "Select Patient",
                                "OK"
                            );
                        } else {
                           
                        }
                    }
                });
            }
        }, 5000); // 5-second delay
    },

    patient_id: function (frm) {
        if (frm.doc.patient_id) {
            frm.trigger("fetch_patient_data");
        }
    },

    fetch_patient_data: function (frm) {
        frappe.call({
            method: "frappe.client.get",
            args: {
                doctype: "Patient Record",
                name: frm.doc.patient_id
            },
            callback: function (response) {
                let patient = response.message;
                if (patient) {
                    // Fetch and allow editing
                    frm.set_value("patient_name", patient.patient_name);
                    frm.set_value("age", patient.age);
                    frm.set_value("gender", patient.gender);
                    frm.set_value("weight", patient.weight);
                    frm.set_value("father_name", patient.father_name);
                    frm.set_value("cnic", patient.cnic);
                    frm.set_value("phone_number", patient.contact_number);
		    frm.set_value("address", patient.address);

                    // Ensure fields are editable
                    ["patient_name", "age", "gender", "weight", "father_name", "cnic", "phone_number", "address", "emergency"].forEach(field => {
                        frm.set_df_property(field, "read_only", 0);
                    });
                }
            }
        });
    },

    after_save: function (frm) {
        if (frm.doc.patient_id) {
            frappe.call({
                method: "frappe.client.set_value",
                args: {
                    doctype: "Patient Record",
                    name: frm.doc.patient_id,
                    fieldname: {
                        "patient_name": frm.doc.patient_name,
                        "age": frm.doc.age,
                        "gender": frm.doc.gender,
                        "weight": frm.doc.weight,
                        "father_name": frm.doc.father_name,
                        "cnic": frm.doc.cnic,
                        "phone_number" : frm.doc.contact_number,
			"address": frm.doc.address
                    }
                },
                callback: function () {
                    
                }
            });
        }
    }
});

frappe.ui.form.on('Emergency', {
    years: function(frm) {
        update_age_and_dob(frm);
    },
    months: function(frm) {
        update_age_and_dob(frm);
    },
    days: function(frm) {
        update_age_and_dob(frm);
    }
});

function update_age_and_dob(frm) {
    let age_parts = [];

    let years = frm.doc.years || 0;
    let months = frm.doc.months || 0;
    let days = frm.doc.days || 0;

    if (years) age_parts.push(`${years} years`);
    if (months) age_parts.push(`${months} months`);
    if (days) age_parts.push(`${days} days`);

    frm.set_value('age', age_parts.join(' '));

    // Calculate Date of Birth
    let today = new Date();
    today.setFullYear(today.getFullYear() - years);
    today.setMonth(today.getMonth() - months);
    today.setDate(today.getDate() - days);

    let formatted_dob = ("0" + today.getDate()).slice(-2) + "-" + 
                        ("0" + (today.getMonth() + 1)).slice(-2) + "-" + 
                        today.getFullYear();

    frm.set_value('date_of_birth', formatted_dob);
}
frappe.ui.form.on('Emergency', {
    refresh: function(frm) {
        // Add a custom button in the Patient Appointment form
        frm.add_custom_button('Create New Patient', function() {
            frappe.new_doc('Patient Appointment'); // Opens a new Patient form
        }, 'Actions'); // Group under 'Actions'

        frm.add_custom_button('View Appointments', function() {
            frappe.set_route('List', 'Patient Appointment'); // Navigates to the Patient Appointment list
        }, 'Actions'); // Group under 'Actions'
    }
});

frappe.ui.form.on('Emergency', {
    after_save: function(frm) {
        // Create a custom dialog
        let dialog = new frappe.ui.Dialog({
            title: 'Emergency Submitted',
            fields: [
                {
                    fieldtype: 'HTML',
                    fieldname: 'message',
                    options: `
                        <div>
                            <p>Emergency Appointment has been submitted successfully</p>
                            <a class="btn btn-sm btn-primary" 
                               href="/api/method/frappe.utils.print_format.download_pdf?doctype=Emergency&name=${frm.doc.name}&format=ER&no_letterhead=0&_lang=English" 
                               target="_blank">Get PDF</a>

                            <a class="btn btn-sm btn-success"  
                               href="/printview?doctype=Emergency&name=${frm.doc.name}&trigger_print=1&format=ER&no_letterhead=0" 
                               target="_blank">Print</a>

                        </div>
                    `
                }
            ],
            primary_action_label: 'Close',
            primary_action: function() {
                dialog.hide();
            }
        });

        dialog.show();

        // Automatically close the dialog after 10 seconds
        setTimeout(() => {
            dialog.hide();
        }, 10000); // 10 seconds
    }
});


frappe.ui.form.on('Emergency', {
    setup: function(frm) {
        // Prevent dropdown list from showing all patient IDs
        frm.set_query("patient_id", function() {
            return {
                filters: { name: ["=", ""] }  // This prevents showing all records
            };
        });
    },

    patient_id: function(frm) {
        if (!frm.doc.patient_id) return;  // Exit if no ID is entered

        frappe.call({
            method: 'frappe.client.get',
            args: {
                doctype: 'Patient Record',  // Ensure this matches the actual Doctype name
                name: frm.doc.patient_id
            },
            callback: function(r) {
                if (r.message) {
                    // Existing patient: Refresh field to fetch details
                    frm.refresh_field("patient_id");
                }
            },
            error: function(err) {
                console.error("Error fetching patient:", err);
            }
        });
    }
});
