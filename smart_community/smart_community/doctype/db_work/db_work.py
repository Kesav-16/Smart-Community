# Copyright (c) 2025, Kesav and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class DBWork(Document):
    def before_naming(self):
        frappe.msgprint("1️⃣ before_naming called")

    def autoname(self):
        frappe.msgprint("2️⃣ autoname called")

    def before_insert(self):
        frappe.msgprint("3️⃣ before_insert called")

    def before_validate(self):
        frappe.msgprint("4️⃣ before_validate called")

    def validate(self):
        frappe.msgprint("5️⃣ validate called")

    def before_save(self):
        frappe.msgprint("6️⃣ before_save called")

    def db_insert(self,ignore_if_duplicate=False                                                                                          ):
        frappe.msgprint("7️⃣ db_insert called")
        return super().db_insert()

    def after_insert(self):
        frappe.msgprint("8️⃣ after_insert called")

    def db_update(self):
        frappe.msgprint("9️⃣ db_update called")
        return super().db_update()

    def on_update(self):
        frappe.msgprint("🔟 on_update called")

    def on_submit(self):
        frappe.msgprint("1️⃣1️⃣ on_submit called")

    def before_submit(self):
        frappe.msgprint("1️⃣2️⃣ before_submit called")

    def before_cancel(self):
        frappe.msgprint("1️⃣3️⃣ before_cancel called")

    def on_cancel(self):
        frappe.msgprint("1️⃣4️⃣ on_cancel called")

    def before_update_after_submit(self):
        frappe.msgprint("1️⃣5️⃣ before_update_after_submit called")

    def on_update_after_submit(self):
        frappe.msgprint("1️⃣6️⃣ on_update_after_submit called")

    def on_change(self):
        frappe.msgprint("1️⃣7️⃣ on_change called")

    # 👉 New methods for rename + delete
    def before_rename(self, olddn, newdn, merge=False):
        frappe.msgprint(f"1️⃣8️⃣ before_rename called: {olddn} → {newdn}")

    def after_rename(self, olddn, newdn, merge=False):
        frappe.msgprint(f"1️⃣9️⃣ after_rename called: {olddn} → {newdn}")

    def on_trash(self):
        frappe.msgprint("2️⃣0️⃣ on_trash called")

    def after_delete(self):
        frappe.msgprint("2️⃣1️⃣ after_delete called")
