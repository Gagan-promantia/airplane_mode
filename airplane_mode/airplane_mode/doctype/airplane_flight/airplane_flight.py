# Copyright (c) 2025, airplane mode and contributors
# For license information, please see license.txt

# import frappe
from frappe.website.website_generator import WebsiteGenerator


class AirplaneFlight(WebsiteGenerator):
	def on_submit(self):
		self.status="Completed"

	def get_context(self, context):
		context.no_cache = 1
		return context