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
        table_html = """
            <h4 style="margin-top:20px; color:#4a90e2;">Consumption Details</h4>
            <table style="width:100%; border-collapse: collapse; font-size:13px; text-align:center;" border="1" cellpadding="6">
            <thead style="background:#f0f6ff;">
                <tr>
                <th style="padding:8px;">Utility</th>
                <th style="padding:8px;">Units</th>
                <th style="padding:8px;">Rate</th>
                <th style="padding:8px;">Amount</th>
                </tr>
            </thead>
            <tbody>
        """

        for bill_row in self.items:
            if bill_row.consumption_log:
                log = frappe.get_doc("Consumption Log", bill_row.consumption_log)
                if log and log.consumption_items:
                    for li in log.consumption_items:
                        table_html += f"""
                            <tr>
                                <td style="padding:8px;">{li.utility or ''}</td>
                                <td style="padding:8px; text-align:center;">{li.units or 0}</td>
                                <td style="padding:8px; text-align:center;">{frappe.format_value(li.rate or 0, {"fieldtype":"Currency"})}</td>
                                <td style="padding:8px; text-align:right; font-weight:bold;">{frappe.format_value(li.amount or 0, {"fieldtype":"Currency"})}</td>
                            </tr>
                        """

        table_html += "</tbody></table>"
        payment_url = f"{frappe.utils.get_url()}/pay_bill?bill_name={self.name}"

        subject = f"Bill Generated: {self.name}"
        total_with_late = getattr(self, "total_with_late", self.total_amount or 0)
        late_fee_amount = getattr(self,"late_fee_amount", 0)

        message = f"""
            <p>Dear {self.resident},</p>
            <p>Your bill <b>{self.name}</b> has been generated for a total of 
            <b>{frappe.format_value(total_with_late, {"fieldtype": "Currency"})}</b>.</p>
            <p> Due Amount:<b>{frappe.format_value(late_fee_amount, {"fieldtype": "Currency"})}<b></p>

            {table_html}

            <p>Please click the link below to pay:</p>
            <p><a href="{payment_url}" target="_blank" 
                style="background:#007BFF;color:white;padding:10px 15px;text-decoration:none;border-radius:5px;">
                Pay Now
            </a></p>
            <br>
            <p>Thank you,<br>Your Community Management</p>
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

