# Copyright (c) 2025, airplane mode and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _
import random
import re


class AirplaneTicket(Document):
	def before_save(self):
		total=self.flight_price

		if self.add_ons:
			for addon in self.add_ons:
				total+=addon.amount

		self.total_amount=total

		# if not self.seat:
		# 	self.assign_seat()

	def validate(self):
		seen=set()
		unique_addons=[]
		for addon in self.add_ons:
			if addon.item in seen:
				continue
			seen.add(addon.item)
			unique_addons.append(addon)

		self.add_ons=unique_addons

		#to avoid airplane tcket if capacity of flight is full
		if not self.flight:
			frappe.throw("Please select a flight before saving the ticket")

		flight=frappe.get_doc("Airplane Flight",self.flight)

		airplane=frappe.get_doc("Airplane",flight.airplane)
		capacity=airplane.capacity

		ticket_count=frappe.db.count("Airplane Ticket",{"flight":self.flight})

		if self.is_new():
			total_after_adding=ticket_count+1
		else:
			total_after_adding=ticket_count

		if total_after_adding>capacity:
			frappe.throw(f"Cannot create more tickets! The airplane is full (capacity:{capacity}).")


	def before_submit(self):
		if self.status !="Boarded":
			frappe.throw(_("Cannot submit Airplane ticket ,Status must be Boarded."))

	def assign_seat(self):
		existing_tickets=frappe.get_all(
			"Airplane Ticket",
			filters={"flight":self.flight},
			fields=["seat"]
		)
		seat_number=len(existing_tickets)+1
		row=(seat_number -1)//6+1
		column=chr(65+(seat_number-1)%6)
		self.seat=f"{row}{column}"

	def before_insert(self):
		number=random.randint(1,99)
		letter=random.choice(['A','B','C','D','E'])
		self.seat=f"{number}{letter}"

# @frappe.whitelist()
# def validate_and_assign_seat(ticket_name, seat):
#     # Load ticket
#     ticket = frappe.get_doc("Airplane Ticket", ticket_name)

#     # Get flight from ticket automatically
#     flight = ticket.flight

#     if not flight:
#         frappe.throw("Flight is not selected for this ticket")

#     # Your business logic here...
#     # For example:
#     existing = frappe.db.exists(
#         "Airplane Ticket",
#         {"flight": flight, "seat": seat}
#     )

#     if existing:
#         frappe.throw(f"Seat {seat} is already booked for this flight.")

#     # assign seat
#     ticket.seat = seat
#     ticket.save()

#     return {"message": "Seat assigned successfully"}
