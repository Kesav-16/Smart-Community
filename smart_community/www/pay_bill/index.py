import frappe
from urllib.parse import unquote

def get_context(context):
    bill_name = frappe.form_dict.get("bill_name")
    if not bill_name:
        frappe.throw("Bill name is missing in URL")

    bill_name = unquote(bill_name)

    try:
        bill = frappe.get_doc("Bill", bill_name)
    except frappe.DoesNotExistError:
        frappe.throw(f"Bill {bill_name} not found")

    context.bill = bill
    consumption_items = []
    for item in bill.items:
        if item.consumption_log:
            log_items = frappe.get_all(
                "Consumption Log Item",
                filters={"parent": item.consumption_log},
                fields=["utility", "units", "amount"]
            )
            for li in log_items:
                consumption_items.append(li)

    context.consumption_items = consumption_items

    context.key_id = "rzp_test_1DP5mmOlF5G5ag"  
    context.amount_paise = int(float(bill.total_with_late) * 100)

    return context
