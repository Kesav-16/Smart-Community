// Copyright (c) 2025, Kesav and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Utility", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on('Utility', {
    refresh(frm) {
        frm.set_df_property('rate', 'description', '₹ per unit cost');
    }
});
