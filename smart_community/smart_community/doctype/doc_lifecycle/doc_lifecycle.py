# Copyright (c) 2025, Kesav and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class DocLifecycle(Document):
		def before_submit(self):
			# Example: Prevent submission if count is less than 5
			if self.count < 5:
				frappe.throw("Count must be at least 5 to submit this document.")
			# Set status to 'Submitted'
			self.status = "Submitted"
			frappe.msgprint("🚀 before_submit triggered")

		
		def before_cancel(self):
			# Example: Prevent cancellation if status is 'Submitted'
			if self.status == "Submitted":
				frappe.throw("Cannot cancel a submitted document directly.")
			frappe.msgprint("❌ before_cancel triggered")

		def before_update_after_submit(self):
        # Example: Prevent changing status back to 'Draft' after submission
			if self.status == "Draft":
				frappe.throw("Cannot change status back to Draft after submission.")
			frappe.msgprint("✏️ before_update_after_submit triggered")	

		def db_insert(self, *args, **kwargs):
        # Set field values before inserting
			if not self.name1:
				self.name1 = "Ms"
			if not self.status:
				self.status = "Draft"
			if not self.count:
				self.count = 10
			frappe.msgprint(f"🗄️ db_insert triggered with name={self.name}, status={self.status}, count={self.count}")
			super().db_insert(*args, **kwargs)
