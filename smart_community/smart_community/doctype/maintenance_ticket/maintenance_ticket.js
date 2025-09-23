frappe.ui.form.on('Maintenance Ticket', {
    refresh(frm) {
        if (frm.doc.status === "Open") {
            frm.add_custom_button('Assign Me', () => {
                frappe.call({
                    method: "frappe.client.set_value",
                    args: {
                        doctype: "Maintenance Ticket",
                        name: frm.doc.name,
                        fieldname: "assigned_to",
                        value: frappe.session.user
                    },
                    callback: () => frm.reload_doc()
                });
            });
        }
    }
});
