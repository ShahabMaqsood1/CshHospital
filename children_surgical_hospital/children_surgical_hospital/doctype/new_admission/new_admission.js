// Copyright (c) 2024, Shahab Maqsood and contributors
// For license information, please see license.txt

// frappe.ui.form.on("New Admission", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on('Admission Payments', {
    payment_amount: function(frm, cdt, cdn) {
        console.log("Paid Payment Amount field changed");
        calculate_remaining_amount(frm, cdt, cdn);
    },
    total_payment_amount: function(frm, cdt, cdn) {
        console.log("Total Payment Amount field changed");
        calculate_remaining_amount(frm, cdt, cdn);
    }
});

function calculate_remaining_amount(frm, cdt, cdn) {
    let row = locals[cdt][cdn];
    
    console.log("Row Data:", row); // Debugging: Log row data
    console.log("Total Payment Amount:", row.total_payment_amount);
    console.log("Paid Payment Amount:", row.payment_amount);
    
    row.remarks = (row.total_payment_amount || 0) - (row.payment_amount || 0);
    
    console.log("Calculated Remaining Amount:", row.remarks); // Debugging: Log calculated value

    frm.refresh_field("payments"); // Refresh child table to update UI
}

frappe.ui.form.on('New Admission', {
    refresh: function(frm) {
        console.log('Form refreshed, docstatus:', frm.doc.docstatus);  // Debugging

        // Check if the document is submitted
        if (frm.doc.docstatus == 1) {
            console.log('Document is submitted.');

            // Make the entire child table read-only for everyone
            frm.set_df_property('payments', 'read_only', true);
            console.log('Payments table set to read-only.');

            // Check if the user is not Shahab
            if (frappe.session.user !== "randeljack123@gmail.com") {
                console.log('User is not Shahab, setting payment_amount to read-only.');
                // Set payment_amount field in the child table to read-only
                frm.fields_dict['payments'].grid.get_field('payment_amount').df.read_only = 1;
                frm.fields_dict['payments'].grid.refresh();
            } else {
                console.log('User is Shahab, allowing editing of payment_amount.');
                // If user is Shahab, allow editing
                frm.fields_dict['payments'].grid.get_field('payment_amount').df.read_only = 0;
                frm.fields_dict['payments'].grid.refresh();
            }
        } else {
            console.log('Document is not submitted, allowing editing.');
            // If document is not submitted, allow editing for everyone
            frm.fields_dict['payments'].grid.get_field('payment_amount').df.read_only = 0;
            frm.fields_dict['payments'].grid.refresh();
        }
    }
});
// Copyright (c) 2024, Shahab Maqsood and contributors
// For license information, please see license.txt
let phoneSearchTimeout;

frappe.ui.form.on("New Admission", {
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


frappe.ui.form.on('New Admission', {
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
