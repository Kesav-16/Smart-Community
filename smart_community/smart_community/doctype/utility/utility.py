# Copyright (c) 2025, Kesav and contributors
# For license information, please see license.txt

import frappe	
from frappe.model.document import Document

class Utility(Document):
    def validate(self):
        if self.rate <= 0:
            frappe.throw("Rate must be greater than 0")
