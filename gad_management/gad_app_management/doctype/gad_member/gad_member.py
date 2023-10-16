# Copyright (c) 2023, Luis Pillaga and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class GadMember(Document):

	def before_save(self):
		"""
		Set full name before saving
		"""
		self.full_name = self.get_full_name()

	def get_full_name(self):
		return f"{self.first_name} {self.last_name}"
