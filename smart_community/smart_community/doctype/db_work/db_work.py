# Copyright (c) 2025, Kesav and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class DBWork(Document):
    # def db_insert(self, *args, **kwargs):
    #     if not self.name1	:
    #         self.name1 = frappe.generate_hash(length=10)
    #     if not hasattr(self, "status") or not self.status:
    #         self.status = "Draft"
    #     if not hasattr(self, "count") or not self.count:
    #         self.count = 1
    #     frappe.msgprint(f"🗄️ db_insert triggered with name={self.name}, status={self.status}, count={self.count}")
    #     super().db_insert(*args, **kwargs)

    # def after_insert(self):
    #     frappe.msgprint(f"✅ Document '{self.name}' inserted with status '{self.status}' and count '{self.count}'.")

    # def db_update(self, *args, **kwargs):
    #     frappe.db.set_value(self.doctype, self.name, {
    #         "status": self.status,
    #         "count": self.count
    #     })
    #     frappe.msgprint(f"🔄 db_update triggered for {self.name} with status '{self.status}' and count '{self.count}'")
    #     super().db_update(*args, **kwargs)
    
	

    def on_update(self):
        frappe.msgprint(f"📝 on_update triggered for {self.name} with status '{self.status}' and count '{self.count}'")

    # def on_submit(self):
    #     frappe.msgprint(f"🚀 on_submit triggered for {self.name} with status '{self.status}' and count '{self.count}'")

    # def on_cancel(self):
    #     frappe.msgprint(f"❌ on_cancel triggered for {self.name} with status '{self.status}' and count '{self.count}'")

    # def on_update_after_submit(self):
    #     frappe.msgprint(f"✏️ on_update_after_submit triggered for {self.name} with status '{self.status}' and count '{self.count}'")

    # def on_change(self):
    #     frappe.msgprint(f"🔔 on_change triggered for {self.name} with status '{self.status}' and count '{self.count}'")

    def before_save(self):
        frappe.msgprint(f"💾 after_save triggered for {self.name} with status '{self.status}' and count '{self.count}'")
