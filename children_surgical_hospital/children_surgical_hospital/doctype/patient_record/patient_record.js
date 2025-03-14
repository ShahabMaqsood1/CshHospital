// Copyright (c) 2024, Shahab Maqsood and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Patient Record", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on("Patient Record", {
    refresh: function(frm) {
        if (frm.is_new()) {
            generate_patient_id(frm);
        }
    },
    emergency: function(frm) {
        generate_patient_id(frm);
    }
});

function generate_patient_id(frm) {
    let is_emergency = frm.doc.emergency || 0;
    let current_year = new Date().getFullYear();

    frappe.call({
        method: "frappe.client.get_value",
        args: {
            doctype: "Patient Numbering",
            fieldname: is_emergency ? "last_number_er" : "last_number"
        },
        callback: function(response) {
            if (response.message) {
                let last_number = response.message[is_emergency ? "last_number_er" : "last_number"] || 0;
                let new_number = last_number + 1;
                let patient_id = is_emergency
                    ? `CSH-${new_number.toString().padStart(5, "0")}-${current_year}-ER`
                    : `CSH-${new_number.toString().padStart(5, "0")}-${current_year}`;

                frm.set_value("patient_id", patient_id);  // ✅ Storing in patient_id field
            }
        }
    });
}

// frappe.ui.form.on('Patient Record', {
//     years: function(frm) {
//         update_age_and_dob(frm);
//     },
//     months: function(frm) {
//         update_age_and_dob(frm);
//     },
//     days: function(frm) {
//         update_age_and_dob(frm);
//     },
//     date_of_birth: function(frm) {
//         update_age_fields(frm);
//     }
// });

// function update_age_and_dob(frm) {
//     let years = frm.doc.years || 0;
//     let months = frm.doc.months || 0;
//     let days = frm.doc.days || 0;

//     let today = new Date();
//     today.setFullYear(today.getFullYear() - years);
//     today.setMonth(today.getMonth() - months);
//     today.setDate(today.getDate() - days);

//     let dob = today.toISOString().split('T')[0]; 

//     frm.set_value('date_of_birth', dob);
//     frm.set_value('age', format_age(years, months, days));
// }

// function update_age_fields(frm) {
//     if (!frm.doc.date_of_birth) return;

//     let dob = frappe.datetime.str_to_obj(frm.doc.date_of_birth);
//     let today = new Date();
    
//     let years = today.getFullYear() - dob.getFullYear();
//     let months = today.getMonth() - dob.getMonth();
//     let days = today.getDate() - dob.getDate();

//     if (days < 0) {
//         months -= 1;
//         days += new Date(today.getFullYear(), today.getMonth(), 0).getDate();
//     }
//     if (months < 0) {
//         years -= 1;
//         months += 12;
//     }

//     frm.set_value('years', years);
//     frm.set_value('months', months);
//     frm.set_value('days', days);
//     frm.set_value('age', format_age(years, months, days));
// }

// function format_age(years, months, days) {
//     let age_parts = [];
//     if (years > 0) age_parts.push(`${years} years`);
//     if (months > 0) age_parts.push(`${months} months`);
//     if (days > 0) age_parts.push(`${days} days`);

//     return age_parts.join(' ');
// }
