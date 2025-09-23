import frappe
from frappe.model.document import Document

class Payment(Document):
    def validate(self):
        if self.bill:
            bill_total = frappe.db.get_value("Bill", self.bill, "total_with_late")
            self.amount = bill_total