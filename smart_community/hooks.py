app_name = "smart_community"
app_title = "Smart Community"
app_publisher = "Kesav"
app_description = "A system to manage residents in a society/apartment, track their utility consumption, generate bills, and manage maintenance requests."
app_email = "kesav@gmail.com"
app_license = "mit"

doc_events = {
    # Maintenance Ticket assignment
    "Maintenance Ticket": {
        "on_update": "smart_community.smart_community.doctype.maintenance_ticket.maintenance_ticket.on_ticket_update"
    }

}

app_include_js = [
    "https://checkout.razorpay.com/v1/checkout.js"
]