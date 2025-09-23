# Copyright (c) 2025, Kesav and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Resident(Document):
    def before_insert(self):
        if not self.full_name:
            frappe.throw("Full Name is required for Resident")

    def after_insert(self):
        frappe.msgprint(f"Resident {self.full_name} created successfully")

    def validate(self):
        if self.phone and not self.phone.isdigit():
            frappe.throw("Phone number must contain only digits")
