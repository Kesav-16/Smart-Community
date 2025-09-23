// Copyright (c) 2025, Kesav and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Resident Utility", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on('Resident Utility', {
    refresh(frm) {
        frm.add_custom_button('View Consumption Logs', () => {
            frappe.set_route('List', 'Consumption Log', { resident: frm.doc.resident });
        });
    }
});
