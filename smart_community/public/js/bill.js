frappe.ui.form.on('Bill', {
  refresh(frm) {
    if (!frm.is_new()) {
      frm.add_custom_button('Recalculate', () => {
        frm.save();
      });
      frm.add_custom_button('Mark Paid', () => {
        frm.set_value('status', 'Paid');
        frm.save();
      });
    }
  }
});

frappe.ui.form.on('Bill Item', {
  units(frm, cdt, cdn) {
    compute_line(frm, cdt, cdn);
  },
  rate(frm, cdt, cdn) {
    compute_line(frm, cdt, cdn);
  }
});

function compute_line(frm, cdt, cdn) {
  const row = frappe.get_doc(cdt, cdn);
  row.amount = flt(row.units) * flt(row.rate);
  frm.refresh_field('items');

  let total = 0;
  (frm.doc.items || []).forEach(r => total += flt(r.amount));
  frm.set_value('total_amount', total);
}
