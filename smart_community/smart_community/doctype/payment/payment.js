frappe.ui.form.on('Payment', {
    refresh(frm) {
        if (frm.doc.bill) {
            frm.add_custom_button('View Bill', () => {
                frappe.set_route('Form', 'Bill', frm.doc.bill);
            });
        }
    }
});
