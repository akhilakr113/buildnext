# Copyright (c) 2026, akhila and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import validate_email_address
from erpnext.selling.doctype.customer.customer import make_address, make_contact
from frappe.model.mapper import get_mapped_doc
from india_compliance.gst_india.utils import validate_gstin

class VendorOnboardingRequest(Document):
	def validate(self):
		validate_email_address(self.email, throw=True)
		validate_gstin(self.gst_number)
		self.validate_annual_turnover()
		self.validate_doccuments_submitted()

	def on_submit(self):
		if self.workflow_state == "Approved":
			self.create_supplier()

	def on_cancel(self):
		existing = frappe.db.get_value(
			"Supplier",
			{"vendor_request": self.name},
			"name"
		)

		frappe.throw(_("Supplier {0} linked to current doccument").format(existing))

	def validate_annual_turnover(self):
		if self.annual_turnover is not None and self.annual_turnover < 0:
			frappe.throw(_("Annual Turnover cannot be negative"))

	def validate_doccuments_submitted(self):
		if self.workflow_state != "Draft" and not self.doccuments_submitted:
			frappe.throw(_("Please check Documents Submitted before submitting."))

	def create_supplier(self):
		existing = frappe.db.get_value(
			"Supplier",
			{"vendor_request": self.name},
			"name"
		)

		if not existing:
			existing = frappe.db.get_value(
				"Supplier",
				{"supplier_name": self.vendor_name},
				"name"
			)

		if existing:
			supplier = frappe.get_doc("Supplier", existing)
			frappe.throw(_("Supplier {0} already exists").format(supplier.name))
		else:
			supplier = frappe.get_doc({
				"doctype": "Supplier",
				"supplier_name": self.vendor_name,
				"supplier_type": self.vendor_category,
				"supplier_category": self.vendor_type,
				"gstin": self.gst_number,
				"vendor_request": self.name,
			})
			supplier.insert(ignore_permissions=True)

			frappe.msgprint(_("Supplier {0} Created Successfully").format(supplier.name))
