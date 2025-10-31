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

add_to_apps_screen = [
    {
        "name": "smart-community",  
        "logo": "/assets/smart_community/img/kes_logo.png",  
        "title": "Smart Community",  
        "route": "/",  
    },
      {
        "name": "About",  
        "logo": "/assets/smart_community/img/kes_logo.png",  
        "title": "About",  
        "route": "/about",  
    }
]

# "host_name": "http://127.0.0.1:8001",

# scheduler_events = {
#     "daily": [
#         "smart_community.smart_community.doctype.bill.bill_reminder.send_unpaid_bill_reminders"
#     ],
#     # Optional: for testing every 10 minutes (remove this in production)
#     "cron": {
#         "*/10 * * * *": [
#             "smart_community.smart_community.doctype.bill.bill_reminder.send_unpaid_bill_reminders"
#         ]
#     }
# }

scheduler_events = {
    "daily": [
        "smart_community.smart_community.doctype.bill.bill_reminder.send_unpaid_bill_reminders"
    ]
}

doctype_js = {
    "Bill": "smart_community/smart_community/doctype/bill/bill_list.js"
}

app_include_js = [
    "/assets/smart_community/js/maintenance_dashboard.js"
]

fixtures=[
    {
        "doctype": "Resident",
        "filters": [["name", "in", ["Dhamo"]]]
    }
]