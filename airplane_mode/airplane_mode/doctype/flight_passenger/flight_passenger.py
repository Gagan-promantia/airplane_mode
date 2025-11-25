# Copyright (c) 2025, airplane mode and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class FlightPassenger(Document):
	
	def before_save(self):
		first_name=self.first_name 
		last_name=self.last_name
		self.full_name=(first_name + " "+last_name).strip()
