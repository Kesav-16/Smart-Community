import frappe
from frappe.model.document import Document
from frappe.utils import nowdate

try:
    import razorpay
except ImportError:
    razorpay = None


class Bill(Document):
    def before_insert(self):
        if not self.items:
            self.populate_items()
        self.calculate_total()

    def before_save(self):
        self.calculate_total()

    def after_insert(self):
        self.send_bill_notification()

    def populate_items(self):
        if self.items:
            return

        logs = frappe.get_all(
            "Consumption Log",
            filters={"resident": self.resident},
            fields=["name", "utility", "units"]
        )

        for log in logs:
            item = self.append("items", {})
            item.consumption_log = log.name
            item.utility = log.utility
            item.units = log.units or 0
            item.rate = frappe.db.get_value("Utility", log.utility, "rate") or 0
            item.amount = (item.units or 0) * (item.rate or 0)

    def calculate_total(self):
        total = 0.0
        for d in self.items:
            try:
                total += d.amount or 0.0
            except Exception:
                total += 0.0
        self.total_amount = total

    def send_bill_notification(self):
        if not self.resident:
            return

        email = frappe.db.get_value("Resident", self.resident, "email")
        if not email:
            frappe.log_error(f"No email found for Resident {self.resident}", "Bill Notification")
            return

        # Build table rows with alternating row colors
        table_rows = ""
        consumption_total = 0
        row_color = ["#ffffff", "#f9f9f9"]  # alternating row colors
        idx = 0

        for bill_row in self.items:
            if bill_row.consumption_log:
                log = frappe.get_doc("Consumption Log", bill_row.consumption_log)
                if log and log.consumption_items:
                    for li in log.consumption_items:
                        amount = li.amount or 0
                        consumption_total += amount
                        bg_color = row_color[idx % 2]
                        table_rows += f"""
                            <tr style="background:{bg_color};">
                                <td style="padding:10px; text-align:left;">{li.utility or ''}</td>
                                <td style="padding:10px; text-align:center;">{li.units or 0}</td>
                                <td style="padding:10px; text-align:right;">{frappe.format_value(li.rate or 0, {"fieldtype":"Currency"})}</td>
                                <td style="padding:10px; text-align:right; font-weight:bold;">{frappe.format_value(amount, {"fieldtype":"Currency"})}</td>
                            </tr>
                        """
                        idx += 1

        table_html = f"""
            <table style="width:100%; border-collapse:collapse; font-family:Arial, sans-serif; font-size:14px; border:1px solid #ddd; margin-top:15px;">
                <thead style="background:linear-gradient(90deg, #4a90e2, #50e3c2); color:white;">
                    <tr>
                        <th style="padding:12px; text-align:left; border:1px solid #ccc;">Utility</th>
                        <th style="padding:12px; text-align:center; border:1px solid #ccc;">Units</th>
                        <th style="padding:12px; text-align:right; border:1px solid #ccc;">Rate</th>
                        <th style="padding:12px; text-align:right; border:1px solid #ccc;">Amount</th>
                    </tr>
                </thead>
                <tbody>
                    {table_rows}
                </tbody>
            </table>
        """

        payment_url = f"{frappe.utils.get_url()}/pay_bill?bill_name={self.name}"
        subject = f"Your Smart Community Bill: {self.name}"

        total_with_late = getattr(self, "total_with_late", self.total_amount or 0)
        late_fee_amount = getattr(self,"late_fee_amount", 0)

        # Modern email HTML theme
        message = f"""
        <div style="font-family:Arial, sans-serif; background:#f0f4f8; padding:30px;">
            <div style="max-width:650px; margin:0 auto; background:white; border-radius:15px; overflow:hidden; box-shadow:0 8px 25px rgba(0,0,0,0.12);">
                
                <!-- Header -->
                <div style="background:linear-gradient(135deg, #4a90e2, #50e3c2); color:white; padding:25px; text-align:center;">
                    <h1 style="margin:0; font-size:24px;">📄 Your Bill is Ready!</h1>
                    <p style="margin:5px 0 0; font-size:14px;">Smart Community Automated Billing</p>
                </div>

                <!-- Bill Info -->
                <div style="padding:25px; color:#333;">
                    <p>Dear <b>{self.resident}</b>,</p>
                    <p>Your bill <b>{self.name}</b> has been generated.</p>

                    <p><b>Total Amount (including late fee if any):</b> <span style="color:#1a73e8;">{frappe.format_value(total_with_late, {"fieldtype":"Currency"})}</span></p>
                    <p><b>Late Fee Amount:</b> <span style="color:#e74c3c;">{frappe.format_value(late_fee_amount, {"fieldtype":"Currency"})}</span></p>

                    <!-- Consumption Table -->
                    {table_html}

                    <!-- Total Consumption -->
                    <p style="text-align:right; font-weight:bold; font-size:14px; margin-top:15px;">
                        Consumption Log Total (without late fee): <span style="color:#34a853;">{frappe.format_value(consumption_total, {"fieldtype":"Currency"})}</span>
                    </p>

                    <!-- Payment Button -->
                    <p style="text-align:center; margin:25px 0;">
                        <a href="{payment_url}" target="_blank" 
                            style="background:#50e3c2; color:white; padding:12px 30px; text-decoration:none; border-radius:10px; font-weight:bold; display:inline-block; box-shadow:0 4px 12px rgba(0,0,0,0.15);">
                            Pay Now
                        </a>
                    </p>

                    <p style="font-size:12px; color:#888;">If you did not expect this bill, please contact your community management immediately.</p>
                    <p>Thank you,<br><b>Smart Community Management Team</b></p>
                </div>
            </div>
        </div>
        """

        frappe.sendmail(
            recipients=[email],
            subject=subject,
            message=message,
            now=True
        )

        return {"status": "Sent"}




@frappe.whitelist()
def mark_bill_paid(bill, payment_id):
    """
    Mark the Bill as Paid, create a Payment record,
    and auto-submit the Bill.
    """
    try:
        bill_doc = frappe.get_doc("Bill", bill)
        bill_doc.status = "Paid"
        if bill_doc.docstatus == 0:
            bill_doc.submit()
        else:
            bill_doc.save(ignore_permissions=True)

        payment_doc = frappe.get_doc({
            "doctype": "Payment",
            "bill": bill_doc.name,
            "payment_mode": "Razorpay",
            "payment_id": payment_id,
            "date": nowdate(),
            "amount": bill_doc.total_amount,
            "status": "Completed"
        })
        payment_doc.insert(ignore_permissions=True)

        frappe.db.commit()
        return {"status": "Paid and Submitted"}

    except Exception as e:
        frappe.log_error(message=str(e), title="Bill Payment Error")
        frappe.throw("Error creating Payment record. Check Error Log.")


@frappe.whitelist()
def create_razorpay_order(bill):
    bill_doc = frappe.get_doc("Bill", bill)
    key_id = frappe.db.get_single_value("Razorpay Settings", "key_id")
    key_secret = frappe.db.get_single_value("Razorpay Settings", "key_secret")
    client = razorpay.Client(auth=(key_id, key_secret))

    amount_paise = int(float(bill_doc.total_amount) * 100)

    order = client.order.create({
        "amount": amount_paise,
        "currency": "INR",
        "payment_capture": 1
    })

    return {
        "order_id": order["id"],
        "amount": amount_paise,
        "bill": bill_doc.name,
        "key": key_id
    }

