// Copyright (c) 2024, Shahab Maqsood and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Lab Reports", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on('Lab Reports', {
    onload: function(frm) {
        frm.set_query('check_patient_no', function() {
            return {
                filters: [
                    ['Check Patient', 'docstatus', '=', 1], // Only submitted (docstatus = 1)
                    ['Check Patient', 'modified', '>=', frappe.datetime.now_date() + ' 00:00:00'], // Today’s date
                    ['Check Patient', 'modified', '<=', frappe.datetime.now_date() + ' 23:59:59']  // Before tomorrow
                ]
            };
        });
    }
});

frappe.ui.form.on('Lab Reports', {
    check_patient_no: function(frm) {
        // Ensure that the 'check_patient_no' is filled before proceeding
        if (!frm.doc.check_patient_no) {
            frappe.msgprint('Please select a Check Patient record.');
            return;
        }

        // Fetch lab_tests directly from the Check Patient Doctype
        frappe.db.get_doc('Check Patient', frm.doc.check_patient_no)
            .then(check_patient_doc => {
                if (check_patient_doc && check_patient_doc.lab_tests) {
                    // Clear the current lab_tests field in Lab Reports before populating it
                    frm.set_value('lab_tests', []);

                    // Loop through the lab_tests from Check Patient and add them to Lab Reports
                    check_patient_doc.lab_tests.forEach(lab_test => {
                        frm.add_child('lab_tests', {
                            'lab_tests': lab_test.lab_tests // Adjust field name if necessary
                        });
                    });

                    // Refresh the field to display the updated lab_tests table
                    frm.refresh_field('lab_tests');
                    frappe.msgprint('Lab tests data fetched successfully.');
                } else {
                    frappe.msgprint('No lab tests found for this Check Patient.');
                }
            })
            .catch(error => {
                console.log('Error fetching Check Patient record:', error);
                frappe.msgprint('Failed to fetch Check Patient record.');
            });
    }
});
frappe.ui.form.on('Lab Reports', {
    refresh: function(frm) {
        console.log('Form refreshed, docstatus:', frm.doc.docstatus);  // Debugging

        // Check if the document is submitted
        if (frm.doc.docstatus == 1) {
            console.log('Document is submitted.');

            // Make the entire child table read-only for everyone
            frm.set_df_property('lab_tests', 'read_only', true);
            console.log('Lab test table set to read-only.');

            // Check if the user is not Shahab (admin)
            if (frappe.session.user !== "Administrator") {
                console.log('User is not Shahab, setting payment_amount to read-only.');
                
                // Set payment_amount field in the child table to read-only for non-admin users
                $.each(frm.doc.lab_tests || [], function(i, row) {
                    frm.fields_dict['lab_tests'].grid.get_field('payment_amount').df.read_only = 1;
                });
                frm.fields_dict['lab_tests'].grid.refresh();
            } else {
                console.log('User is Shahab, allowing editing of payment_amount.');

                // Allow editing of payment_amount for admin (Shahab)
                $.each(frm.doc.lab_tests || [], function(i, row) {
                    frm.fields_dict['lab_tests'].grid.get_field('payment_amount').df.read_only = 0;
                });
                frm.fields_dict['lab_tests'].grid.refresh();
            }
        } else {
            console.log('Document is not submitted, allowing editing.');

            // If document is not submitted, allow editing for everyone
            $.each(frm.doc.lab_tests || [], function(i, row) {
                frm.fields_dict['lab_tests'].grid.get_field('payment_amount').df.read_only = 0;
            });
            frm.fields_dict['lab_tests'].grid.refresh();
        }
    }
});
frappe.ui.form.on('Lab Reports', {
    after_save: function(frm) {
        // Log the patient_id to ensure it's correct
        console.log("Patient ID from Lab Reports form: " + frm.doc.patient_id);

        // Fetch the Patient Record based on the patient_id
        frappe.db.get_value('Patient Record', { 'name': frm.doc.patient_id }, 'name')
            .then(r => {
                if (r.message && r.message.name) {
                    let patient_record_name = r.message.name;
                    console.log("Patient Record found: " + patient_record_name);

                    // Fetch the Patient Record document
                    frappe.db.get_doc('Patient Record', patient_record_name)
                        .then(patient_record_doc => {
                            console.log("Patient Record document details: ", patient_record_doc);

                            // Loop through the lab_tests table in Lab Reports
                            frm.doc.lab_tests.forEach(lab_test => {
                                // Check if the lab test already exists in the Patient Record
                                let existing_test = patient_record_doc.lab_tests.find(test => 
                                    test.lab_tests === lab_test.lab_tests // Compare lab test identifier
                                );

                                if (existing_test) {
                                    // If the lab test exists, update the upload_results field
                                    existing_test.upload_results = lab_test.upload_results;
                                    console.log("Updated existing lab test: " + lab_test.lab_tests + " with new results.");
                                } else {
                                    // If the lab test doesn't exist, append it to the Patient Record
                                    patient_record_doc.lab_tests.push({
                                        "lab_tests": lab_test.lab_tests, // Store lab test name
                                        "upload_results": lab_test.upload_results // Store lab test result
                                    });
                                    console.log("Added new lab test: " + lab_test.lab_tests);
                                }
                            });

                            // Save the updated Patient Record using frappe.client.save
                            frappe.call({
                                method: "frappe.client.save",
                                args: {
                                    doc: patient_record_doc
                                },
                                callback: function(response) {
                                    frappe.msgprint({
                                        title: _('Success'),
                                        indicator: 'green',
                                        message: __('Patient Record updated successfully.')
                                    });
                                    console.log("Patient Record saved successfully.");
                                },
                                error: function(error) {
                                    frappe.msgprint({
                                        title: __('Error'),
                                        indicator: 'red',
                                        message: __('Failed to update the Patient Record.')
                                    });
                                    console.error("Error saving Patient Record: ", error);
                                }
                            });
                        })
                        .catch(error => {
                            console.error("Error fetching Patient Record: ", error);
                        });
                } else {
                    // If no record found, log and notify the user
                    console.log("No Patient Record found for Patient ID: " + frm.doc.patient_id);
                    frappe.msgprint("No Patient Record found for the given Patient ID.");
                }
            });
    }
});
// Copyright (c) 2024, Shahab Maqsood and contributors
// For license information, please see license.txt

frappe.ui.form.on("Lab Reports", {
refresh(frm) {

	},
});
// Copyright (c) 2024, Shahab Maqsood and contributors
// For license information, please see license.txt
let phoneSearchTimeout;

frappe.ui.form.on("Lab Reports", {
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


frappe.ui.form.on('Lab Reports', {
    after_save: function(frm) {
        // Create a custom dialog
        let dialog = new frappe.ui.Dialog({
            title: 'Lab Report Submitted',
            fields: [
                {
                    fieldtype: 'HTML',
                    fieldname: 'message',
                    options: `
                        <div>
                            <p>Report has been submitted successfully</p>
                            <a class="btn btn-sm btn-primary" 
                               href="/api/method/frappe.utils.print_format.download_pdf?doctype=Lab%20Reports&name=${frm.doc.name}&format=Lab%20Reports&no_letterhead=0&_lang=English" 
                               target="_blank">Get PDF</a>

                            <a class="btn btn-sm btn-success"  
                               href="/printview?doctype=Lab%20Reports&name=${frm.doc.name}&trigger_print=1&format=Lab%20Reports&no_letterhead=0" 
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


frappe.ui.form.on('Lab Reports', {
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

