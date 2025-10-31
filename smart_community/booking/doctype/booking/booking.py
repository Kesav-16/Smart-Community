# Copyright (c) 2025, Kesav and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Booking(Document):
	def validate(self):
		# Automatically join First Name + Last Name into Full Name
		if self.first_name or self.last_name:
			self.full_name = f"{(self.first_name or '').strip()} {(self.last_name or '').strip()}".strip()

