import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname

class DocLifecycleTest(Document):
    def before_naming(self):
        if not self.department:
            self.department = "Guest"

    def autoname(self):
        prefix = self.department.upper() if getattr(self, "department", None) else "GEN"
        self.name = make_autoname(f"{prefix}-.###")

    # def before_rename(self, olddn, newdn, merge=False):
    #     new_doc = frappe.new_doc("Doc Lifecycle Test")
    #     new_doc.title = "Renamed"
    #     new_doc.status = "Draft"
    #     new_doc.count = 0
    #     new_doc.department = "Guest"
    #     new_doc.first_name = "Renamed First"
    #     new_doc.last_name = "Renamed Last"
    #     new_doc.full_name = f"{new_doc.first_name} {new_doc.last_name}"
    #     new_doc.insert()
    #     frappe.msgprint(f"New record created with name: {new_doc.name}")

    def before_insert(self):
        if not self.status:
            self.status = "Draft"
        if not self.count:
            self.count = 1
        if not self.title:
            self.title = " Recordsss"
        frappe.msgprint("📌 before_insert triggered")

    def before_validate(self):
        if not self.full_name and self.first_name and self.last_name:
            self.full_name = f"{self.first_name} {self.last_name}"
        frappe.msgprint("🎈 before_validate triggered")

    def validate(self):
        # Ensure first_name and last_name are present
        if not self.first_name or not self.last_name:
            frappe.throw("First Name and Last Name are required.")

        # Ensure count is positive
        if self.count is not None and self.count <= 0:
            frappe.throw("Count must be greater than zero.")

        # Status must be either 'Draft' or 'Renamed'
        # if self.status not in ["Draft", "Renamed"]:
        #     frappe.throw("Status must be 'Draft' or 'Renamed'.").

        frappe.msgprint("✅ Validation passed.")

    def before_save(self):
        # Example: Set a custom message or update a field before saving
        self.title = f"{self.title} (Ready to Save)"
        frappe.msgprint("💾 before_save triggered")

    def before_submit(self):
        # Example: Prevent submission if count is less than 5
        if self.count < 5:
            frappe.throw("Count must be at least 5 to submit this document.")
        # Set status to 'Submitted'
        self.status = "Submitted"
        frappe.msgprint("🚀 before_submit triggered")

