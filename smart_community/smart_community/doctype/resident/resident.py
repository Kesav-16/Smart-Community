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

@frappe.whitelist()
def approve_and_notify(resident_name, email, full_name):
    # Step 1: Approve the Resident
    frappe.db.set_value("Resident", resident_name, "status", "Approved")
    frappe.db.commit()

    # Step 2: Generate secure token
    import secrets
    token = secrets.token_urlsafe(32)
    frappe.cache().set_value(f"guest_login_{token}", email, expires_in_sec=3600)  # 1 hour

    # Step 3: Build login URL
    login_link = f"{frappe.utils.get_url('/guest-login')}?token={token}&next=/guest-dashboard"

    # Step 4: Send email
    subject = f"Welcome {full_name}! Your Apartment Access is Approved"
    message = f"""
    <p>Dear {full_name},</p>
    <p>Your booking request has been approved 🎉</p>
    <p>Click below to access your dashboard:</p>
    <p><a href="{login_link}" target="_blank">{login_link}</a></p>
    <br>
    <p>Best Regards,<br>Smart Community Team</p>
    """
    frappe.sendmail(recipients=email, subject=subject, message=message)
    return {"status": "success", "msg": "Email sent successfully!"}

