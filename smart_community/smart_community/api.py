# smart_community/smart_community/api.py
import frappe
from datetime import datetime
from frappe.utils import nowdate
import razorpay
from frappe import _

@frappe.whitelist(allow_guest=True)
def register_apartment_user(full_name, email, phone, apartment, password):
    """
    Save user registration with plain password.
    """
    if not (full_name and email and password):
        frappe.throw("Full Name, Email and Password are required.")

    doc = frappe.get_doc({
        "doctype": "Apartment Registration",
        "full_name": full_name,
        "email": email,
        "phone": phone,
        "apartment": apartment,
        "password": password,
        "created_on": datetime.now()
    })
    doc.insert(ignore_permissions=True)
    frappe.db.commit()

    return {"status": "success", "message": "Registered successfully!"}

@frappe.whitelist(allow_guest=True)
def login_apartment_user(email, password):
    """
    Validate user login using Apartment Registration DocType
    """
    email = email.strip().lower()
    password = password.strip()

    user = frappe.db.get_all(
        "Apartment Registration",
        filters={"email": email, "password": password},
        fields=["name", "full_name"]
    )

    if user and len(user) > 0:
        return {"status": "success", "message": f"Welcome {user[0].full_name}!"}
    else:
        return {"status": "fail", "message": "Invalid email or password."}

@frappe.whitelist()
def save_selected_utilities(parent_doctype, parent_name, utilities):
    """
    utilities: list of dicts with keys: utility_type, provider, rate
    parent_doctype: "Resident"
    parent_name: name (ID) of the parent document (returned by web_form after save)
    """
    if not parent_doctype or not parent_name:
        frappe.throw(_("parent_doctype and parent_name are required"))

    # ensure utilities is a list (if sent as JSON string)
    if isinstance(utilities, str):
        import json
        utilities = json.loads(utilities)

    doc = frappe.get_doc(parent_doctype, parent_name)

    # clear existing child rows if you want to replace them
    # doc.set("selected_utilities", [])  # uncomment to clear previous selections

    # Append each selected utility as a child row
    for u in utilities:
        # protect against missing fields
        utility_type = u.get("utility_type") or u.get("type") or u.get("utility")
        provider = u.get("provider") or u.get("provider_name") or ""
        rate = u.get("rate") or 0

        # append child row
        doc.append("selected_utilities", {
            "utility_type": utility_type,
            "provider": provider,
            "rate": rate
        })

    doc.save(ignore_permissions=True)
    frappe.db.commit()

    return {"status": "success", "added": len(utilities)}


@frappe.whitelist(allow_guest=True)
def register_apartment_user(full_name, email, phone, apartment, password):
    """
    Register a new apartment booking:
    1️⃣ Save details in Resident / Apartment Registration
    2️⃣ Create a Frappe User with role "Guest 01" if not exists
    """

    # Validate required fields
    if not (full_name and email and password):
        frappe.throw(_("Full Name, Email, and Password are required."))

    # 1️⃣ Check if a registration already exists
    if frappe.db.exists("Apartment Registration", {"email": email}):
        return {"status": "error", "message": _("You have already registered.")}

    # 2️⃣ Create new Apartment Registration / Resident record
    resident = frappe.get_doc({
        "doctype": "Apartment Registration",  # or "Resident" if you use that DocType
        "full_name": full_name,
        "email": email,
        "phone": phone,
        "apartment": apartment,
        "password": password,  # storing as is
        "created_on": datetime.now()
    })
    resident.insert(ignore_permissions=True)

    # 3️⃣ Create User if not exists
    if not frappe.db.exists("User", email):
        user = frappe.get_doc({
            "doctype": "User",
            "email": email,
            "first_name": full_name.split(" ")[0],
            "full_name": full_name,
            "send_welcome_email": 0,  # 🚫 No email
            "enabled": 1,
            "new_password": password
        })
        # ✅ Assign the role "Guest 01"
        user.append("roles", {"role": "Guest 01"})
        user.insert(ignore_permissions=True)

    # Commit all changes
    frappe.db.commit()

    return {"status": "success", "message": _("Resident and User created successfully")}

@frappe.whitelist(allow_guest=True)
def get_guest_bookings(email):
    """
    Fetch only approved bookings for a guest, along with apartment images.
    """
    if not email:
        return {"error": "No email specified"}

    bookings = frappe.get_all(
        "Resident",
        filters={"email": email, "status": "Approved"},
        fields=["full_name", "apartment", "start_date", "end_date", "status", "phone"]
    )

    if not bookings:
        return {"error": "No approved bookings found"}

    # Add apartment image to each booking
    for b in bookings:
        b["image"] = frappe.get_value("Apartment", b["apartment"], "image") or ""

    return {"bookings": bookings}


@frappe.whitelist(allow_guest=True)
def guest_token_login(token):
    """
    Validate a temporary token from email link and return the guest email.
    """
    email = frappe.cache().get_value(f"guest_login_{token}")
    if not email:
        return {"status": "failed", "error": "Invalid or expired login link."}
    return {"status": "success", "email": email}

@frappe.whitelist(allow_guest=True)
def custom_login(email, password):
    """
    Validate Apartment Registration + Resident approval.
    Returns success if valid, along with email for sessionStorage.
    """
    # 1️⃣ Check Apartment Registration credentials
    user = frappe.db.get_value(
        "Apartment Registration",
        {"email": email},
        ["name", "password"],
        as_dict=True
    )
    if not user:
        return {"status": "failed", "error": "Email not found."}

    if user.password != password:
        return {"status": "failed", "error": "Incorrect password."}

    # 2️⃣ Check Resident approval
    resident = frappe.db.get_value(
        "Resident",
        {"email": email},
        ["name", "status"],
        as_dict=True
    )
    if not resident or resident.status != "Approved":
        return {"status": "failed", "error": "Your account is not approved yet."}

    return {"status": "success", "email": email}


@frappe.whitelist(allow_guest=True)
def get_apartment_bookings(apartment):
    bookings = frappe.get_all(
        "Resident",
        filters={"apartment": apartment, "status": "Approved"},
        fields=["full_name", "email", "phone", "start_date", "end_date", "status"]
    )
    return bookings


@frappe.whitelist()
def get_guest_bills(email):
    """
    Fetch all bills for a guest based on their email.
    Returns a structured list of bills including consumption items and total_with_late.
    """
    if not email:
        return {"bills": []}

    bills = frappe.get_all(
        "Bill",
        filters={"custom_email": email},
        fields=[
            "name",
            "resident",
            "billing_month",
            "billing_year",
            "due_date",
            "status",
            "days_late",
            "late_fee_amount",
            "total_with_late"  # fetch the total directly
        ],
        order_by="billing_year desc, billing_month desc"
    )

    result = []

    for bill in bills:
        # Fetch consumption items (child table)
        items = frappe.get_all(
            "Bill Item",  # Replace with your child table name for consumption details
            filters={"parent": bill.name},
            fields=["consumption_log", "amount"]
        )

        result.append({
            "name": bill.name,
            "resident": bill.resident,
            "billing_month": bill.billing_month,
            "billing_year": bill.billing_year,
            "due_date": bill.due_date,
            "status": bill.status,
            "days_late": bill.days_late,
            "late_fee_amount": bill.late_fee_amount,
            "items": items,
            "total_with_late": bill.total_with_late  # use the field directly
        })

    return {"bills": result}


@frappe.whitelist()
def create_razorpay_order(bill_name):
    """
    Create a Razorpay order for the given bill.
    Returns order_id, amount in paise, bill name, and key_id.
    """
    if not bill_name:
        frappe.throw("Bill name is required")

    bill_doc = frappe.get_doc("Bill", bill_name)
    
    key_id = frappe.db.get_single_value("Razorpay Settings", "key_id")
    key_secret = frappe.db.get_single_value("Razorpay Settings", "key_secret")

    client = razorpay.Client(auth=(key_id, key_secret))

    amount_paise = int(float(bill_doc.total_with_late) * 100)

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


@frappe.whitelist()
def mark_bill_paid(bill_name, payment_id):
    """
    Update Bill status to Paid and create a Payment record
    after successful Razorpay payment.
    """
    try:
        bill_doc = frappe.get_doc("Bill", bill_name)
        bill_doc.status = "Paid"

        if bill_doc.docstatus == 0:
            bill_doc.submit()
        else:
            bill_doc.save(ignore_permissions=True)

        # Create Payment record
        payment_doc = frappe.get_doc({
            "doctype": "Payment",
            "bill": bill_doc.name,
            "payment_mode": "Razorpay",
            "payment_id": payment_id,
            "date": nowdate(),
            "amount": bill_doc.total_with_late or bill_doc.total_amount,
            "status": "Completed"
        })
        payment_doc.insert(ignore_permissions=True)

        frappe.db.commit()
        return {"status": "Paid and Recorded"}

    except Exception as e:
        frappe.log_error(message=str(e), title="Bill Payment Error")
        frappe.throw("Error recording payment. Check error log.")