import frappe
from frappe.utils import getdate, nowdate, get_url

def send_unpaid_bill_reminders():
    """Send daily reminder emails for all unpaid bills that are due or overdue."""

    # Fetch unpaid and overdue bills
    unpaid_bills = frappe.get_all(
        "Bill",
        filters={
            "status": ["!=", "Paid"],
            "docstatus": 1  # Only submitted bills
        },
        fields=["name", "resident", "due_date", "total_amount"]
    )

    today = getdate(nowdate())
    sent_count = 0

    for bill in unpaid_bills:
        try:
            # Skip if no resident
            if not bill.resident:
                continue

            # Skip if due date is in the future
            if bill.due_date and getdate(bill.due_date) > today:
                continue

            resident = frappe.get_doc("Resident", bill.resident)
            if not resident.email:
                frappe.log_error(f"No email for resident {bill.resident}", "Unpaid Bill Reminder")
                continue

            # Check if already sent today
            last_reminder = frappe.db.get_value(
                "Communication",
                {
                    "reference_name": bill.name,
                    "subject": ["like", "%Unpaid Bill Reminder%"]
                },
                "creation"
            )
            if last_reminder and getdate(last_reminder) == today:
                continue  # already sent today

            # Email subject and link
            subject = f"⏰ Reminder: Payment Pending for Bill {bill.name}"
            pay_url = f"{get_url()}/pay_bill?bill_name={bill.name}"

            message = f"""
            <div style="font-family:Arial,sans-serif;background:#f9fafb;padding:30px;">
                <div style="max-width:650px;margin:0 auto;background:white;border-radius:10px;padding:25px;box-shadow:0 5px 20px rgba(0,0,0,0.08);">
                    <h2 style="color:#e74c3c;">⚠ Payment Reminder</h2>
                    <p>Dear <b>{resident.full_name or resident.name}</b>,</p>
                    <p>Your bill <b>{bill.name}</b> amounting to 
                    <b>{frappe.format_value(bill.total_amount, {'fieldtype': 'Currency'})}</b> is still unpaid.</p>
                    <p>The due date was <b>{bill.due_date}</b>. Please make your payment to avoid any late fees.</p>

                    <p style="text-align:center;margin:30px 0;">
                        <a href="{pay_url}" target="_blank"
                        style="background:#50e3c2;color:white;padding:12px 25px;border-radius:8px;text-decoration:none;font-weight:bold;">
                        Pay Now
                        </a>
                    </p>

                    <p style="color:#888;font-size:12px;">This is an automated daily reminder from Smart Community Billing System.</p>
                </div>
            </div>
            """

            # Send email
            frappe.sendmail(
                recipients=[resident.email],
                subject=subject,
                message=message,
                now=True,
                reference_doctype="Bill",
                reference_name=bill.name
            )

            sent_count += 1
            frappe.logger().info(f"✅ Reminder sent for Bill {bill.name}")

        except Exception as e:
            frappe.log_error(f"Error sending reminder for {bill.name}: {str(e)}", "Bill Reminder Error")

    frappe.logger().info(f"📬 Total reminders sent today: {sent_count}")
