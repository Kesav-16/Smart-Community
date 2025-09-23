frappe.ready(() => {
    console.log("Maintenance Ticket Web Form Loaded");

    // Set default status to "Open"
    frappe.web_form.set_value("status", "Open");

    // Example: auto-fill logged-in user into Resident if available
    if (frappe.session.user !== "Guest") {
        frappe.call({
            method: "frappe.client.get",
            args: {
                doctype: "Resident",
                filters: { user_id: frappe.session.user }
            },
            callback: (r) => {
                if (r.message) {
                    frappe.web_form.set_value("resident", r.message.name);
                }
            }
        });
    }

    // Show confirmation after submit
    frappe.web_form.on("after_save", () => {
        frappe.msgprint("✅ Your maintenance request has been submitted!");
    });
});
