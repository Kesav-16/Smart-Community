// Copyright (c) 2025, Kesav and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Resident", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on('Resident', {
    refresh(frm) {
        frm.add_custom_button('View Bills', () => {
            frappe.set_route('List', 'Bill', { resident: frm.doc.name });
        }, 'View');
    }
});
