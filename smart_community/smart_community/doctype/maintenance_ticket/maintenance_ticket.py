import frappe
from frappe.model.document import Document

class MaintenanceTicket(Document):
    pass

def on_ticket_update(doc, _):
    if doc.assigned_to:
        frappe.share.add("Maintenance Ticket", doc.name, doc.assigned_to, read=1, write=1)
    if doc.has_value_changed("assigned_to") and doc.assigned_to:
        frappe.publish_realtime(
            event="msgprint",
            message=f"Ticket {doc.name} assigned to {doc.assigned_to}",
            user=doc.assigned_to
        )
