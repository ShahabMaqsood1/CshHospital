// Copyright (c) 2025, Shahab Maqsood and contributors
// For license information, please see license.txt

// Helper: combine date and time into one datetime string
frappe.datetime.combine_date_and_time = function(date, time) {
    return `${date} ${time}`;
};

frappe.ui.form.on('Discharge Bill', {
    onload: function(frm) {
        frm.trigger('fetch_advance_payment');
    },

    admission_no: function(frm) {
        frm.trigger('fetch_advance_payment');
    },

    fetch_advance_payment: function(frm) {
        if (!frm.doc.admission_no) return;

        frm.set_value('advance', 0); // Temporary default

        frappe.db.get_doc('New Admission', frm.doc.admission_no).then(admission => {
            if (admission) {
                frm.set_value('date_of_admission', admission.date);
                frm.set_value('admit_in', admission.admission_in);
                frm.set_value('admission_fee', 1000); // Default fee

                let total_advance = admission.payments?.reduce((sum, row) => sum + (parseFloat(row.payment_amount) || 0), 0) || 0;
                frm.set_value('advance', total_advance);
                frm.refresh_field('advance');

                frm.trigger('calculate_total');
            }
        });
    },

    date_of_discharge: function(frm) {
        if (frm.doc.date_of_admission && frm.doc.date_of_discharge && frm.doc.time_of_admission && frm.doc.time_of_discharge) {
            let admission_datetime = frappe.datetime.combine_date_and_time(frm.doc.date_of_admission, frm.doc.time_of_admission);
            let discharge_datetime = frappe.datetime.combine_date_and_time(frm.doc.date_of_discharge, frm.doc.time_of_discharge);

            let admission = new Date(admission_datetime);
            let discharge = new Date(discharge_datetime);

            let diff_in_hours = (discharge - admission) / (1000 * 60 * 60); // milliseconds to hours
            let days = parseFloat((diff_in_hours / 24).toFixed(2)); // convert to float days

            frm.set_value('no_of_days', days);
            frm.trigger('calculate_total');
        }
    },

    operation_fee: function(frm) {
        if (frm.doc.operation_fee) {
            frm.set_value('anaethetist_fee', 5000);
            frm.set_value('theater_charges', 5000);
            frm.trigger('calculate_total');
        }
    },

    admit_in: function(frm) {
        if (!frm.doc.no_of_days) return;

        let ward_charges = 0, icu_charges = 0, room_charges = 0;

        if (['Ward 1', 'Ward 2'].includes(frm.doc.admit_in)) {
            ward_charges = frm.doc.no_of_days * 7000;
        }

        if (frm.doc.admit_in === 'ICU') {
            icu_charges = frm.doc.no_of_days * 10000;
        }

        if (['Room 1', 'Room 2', 'Room 3', 'Room 4', 'Room 5', 'Room 6'].includes(frm.doc.admit_in)) {
            room_charges = frm.doc.no_of_days * 10000;
        } else if (frm.doc.admit_in === 'Executive Room') {
            room_charges = frm.doc.no_of_days * 15000;
        }

        frm.set_value('ward_charges', ward_charges);
        frm.set_value('icu_charges', icu_charges);
        frm.set_value('room_charges', room_charges);
        frm.trigger('calculate_total');
    },

    on_oxygen_days: function(frm) {
        frm.set_value('oxygen_charges', (frm.doc.on_oxygen_days || 0) * 7000);
        frm.trigger('calculate_total');
    },

    no_of_days: function(frm) {
        let days = frm.doc.no_of_days || 0;
        frm.set_value('tahir_visiting_fee', days * 3000);
        frm.set_value('abdul_visiting_fee', days * 2000);
        frm.set_value('medical_officer', days * 1000);
        frm.set_value('nursing_care', days * 500);
        frm.trigger('calculate_total');
    },

    validate: function(frm) {
        frm.trigger('calculate_total');
    },

    calculate_total: function(frm) {
        function getNumber(value) {
            return isNaN(parseFloat(value)) ? 0 : parseFloat(value);
        }

        let total = getNumber(frm.doc.admission_fee) + 
                    getNumber(frm.doc.operation_fee) + 
                    getNumber(frm.doc.anaethetist_fee) + 
                    getNumber(frm.doc.theater_charges) + 
                    getNumber(frm.doc.ward_charges) + 
                    getNumber(frm.doc.room_charges) + 
                    getNumber(frm.doc.icu_charges) + 
                    getNumber(frm.doc.tahir_visiting_fee) + 
                    getNumber(frm.doc.abdul_visiting_fee) + 
                    getNumber(frm.doc.abid_visiting_fee) + 
                    getNumber(frm.doc.medical_officer) + 
                    getNumber(frm.doc.nursing_care) + 
                    getNumber(frm.doc.special_services) + 
                    getNumber(frm.doc.medical_charges) + 
                    getNumber(frm.doc.circumcision_charges) + 
                    getNumber(frm.doc.oxygen_charges) + 
                    getNumber(frm.doc.monitoring_charges) + 
                    getNumber(frm.doc.ota_charges);

        frm.set_value('total', total);
        frm.refresh_field('total');

        let grand_total = total - getNumber(frm.doc.advance) - getNumber(frm.doc.discount);
        frm.set_value('grand_total', grand_total);
        frm.refresh_field('grand_total');
    }
});

frappe.ui.form.on('Discharge Bill', {
    setup: function(frm) {
        frm.set_query("admission_no", function() {
            return {
                filters: {
                    docstatus: 0  // Show only Draft (unsaved/submittable) admissions
                }
            };
        });
    }
});
