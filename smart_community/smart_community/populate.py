import frappe
import random

def execute():
    """
    Patch to backfill missing Block and Flat No for existing 'Resident' records
    where both fields are empty and status is 'Approved'.
    Run using:
        bench run-patch your_app.patches.custom.populate_seats
    """

    DOCTYPE = "Resident"
    blocks = ["A", "B", "C", "D"]

    # Fetch residents without block or flat number
    residents = frappe.get_all(
        DOCTYPE,
        filters={
            "status": "Approved",
            "block": ["is", "not set"],
            "flat_no": ["is", "not set"]
        },
        fields=["name"]
    )

    if not residents:
        print("✅ No missing block/flat_no found.")
        return

    for r in residents:
        doc = frappe.get_doc(DOCTYPE, r.name)

        # Assign random block
        block = random.choice(blocks)

        # Generate next unique flat number for that block
        existing_flats = frappe.get_all(
            DOCTYPE,
            filters={"block": block},
            fields=["flat_no"]
        )
        existing_numbers = [
            int(f["flat_no"][1:]) for f in existing_flats
            if f["flat_no"] and f["flat_no"][1:].isdigit()
        ]
        next_number = (max(existing_numbers) + 1) if existing_numbers else 101
        flat_no = f"{block}{next_number}"

        # Save updates
        doc.block = block
        doc.flat_no = flat_no
        doc.save(ignore_permissions=True)

        # ✅ Print only the new values (not record name)
        print(f"Block={block}, Flat No={flat_no}")

    frappe.db.commit()
    print("✅ populate_seats patch executed successfully.")
