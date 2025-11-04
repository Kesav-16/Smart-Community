# Copyright (c) 2025, Kesav and contributors
# For license information, please see license.txt

import secrets
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
def approve_and_notify(resident_name):
    """
    Approve a Resident booking and send confirmation email.
    Only resident_name is required; email and full_name are fetched automatically.
    """

    # Step 1: Fetch resident document
    resident = frappe.get_doc("Resident", resident_name)
    email = resident.email
    full_name = resident.full_name

    if not email or not full_name:
        frappe.throw("Resident record missing email or full name.")

    # Step 2: Approve booking
    resident.status = "Approved"
    resident.save(ignore_permissions=True)
    frappe.db.commit()

    # Step 3: Generate secure login token
    token = secrets.token_urlsafe(32)
    frappe.cache().set_value(f"guest_login_{token}", email, expires_in_sec=3600)  # 1 hour expiry

    # Step 4: Prepare dashboard login URL
    login_link = f"{frappe.utils.get_url('/guest-login')}?token={token}&next=/guest-dashboard"

    # Step 5: Compose and send email
    subject = f"Welcome {full_name}! Your Apartment Access is Approved"
    message = f"""
        <p>Dear {full_name},</p>
        <p>Your apartment booking request has been approved 🎉</p>
        <p>Click below to access your dashboard:</p>
        <p><a href="{login_link}" target="_blank">{login_link}</a></p>
        <br>
        <p>Best Regards,<br>Smart Community Team</p>
    """

    frappe.sendmail(recipients=email, subject=subject, message=message)

    return {"status": "success", "msg": f"Resident {full_name} approved and email sent!"}

