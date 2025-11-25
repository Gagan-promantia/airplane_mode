import frappe
import random

def execute():
    tickets=frappe.get_all("Airplane Ticket",fields={"seat": ["is","not set"]}, pluck="name")
    for ticket_name in tickets:
        number=random.randint(1,99)
        letter=random.choice(['A','B','C','D','E'])
        seat=f"{number}{letter}"

        frappe.db.set_value("Airplane Ticket", ticket_name, "seat", seat)

    frappe.db.commit()
    frappe.msgprint(f"seats have been populated  for {len(tickets)} existing tickets")