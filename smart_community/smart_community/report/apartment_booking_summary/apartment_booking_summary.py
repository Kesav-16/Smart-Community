import frappe
from frappe.query_builder import DocType
from frappe.query_builder.functions import Count

@frappe.whitelist(allow_guest=True)
def execute(filters=None):
    if not filters:
        filters = {}

    registration = DocType("Apartment Registration")

    # Query: Count how many registrations per apartment
    query = (
        frappe.qb.from_(registration)
        .select(
            registration.apartment.as_("apartment"),
            Count(registration.name).as_("total_registrations")
        )
        .groupby(registration.apartment)
        .orderby(Count(registration.name), order=frappe.qb.desc)
    )

    data = query.run(as_dict=True)

    for d in data:
        d["apartment"] = d.get("apartment") or "Unknown"
        d["total_registrations"] = d["total_registrations"] or 0

    # Columns
    columns = [
        {"label": "Apartment", "fieldname": "apartment", "fieldtype": "Data", "width": 300},
        {"label": "Total Registrations", "fieldname": "total_registrations", "fieldtype": "Int", "width": 200},
    ]

    # Summary
    total = sum(d["total_registrations"] for d in data)
    summary = [
        {"label": "Total Registrations", "value": total, "indicator": "Blue"}
    ]

    # ✅ Correct Donut Chart Configuration
    chart = {
        "data": {
            "labels": [d["apartment"] for d in data],
            "datasets": [{
                "name": "Total Registrations",
                "values": [d["total_registrations"] for d in data],
            }],
        },
        "type": "donut",  # 👈 Correct type recognized by Frappe
        "height": 300,
        "colors": ["#3b82f6", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6"],
        "options": {
            "legend": True,
            "truncate_legends": True,
            "donut": True,  # 👈 Frappe uses this flag internally for donut-style
            "donut_width": 60,  # 👈 Width of the donut ring
        }
    }

    return columns, data, None, chart, summary

