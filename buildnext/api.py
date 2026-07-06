import frappe
from frappe import _
from frappe.utils import cint

@frappe.whitelist(methods=["POST"])
def create_request(**kwargs):
	vendor_name = kwargs.get("vendor_name")
	email = kwargs.get("email")
	vendor_type = kwargs.get("vendor_type")

	if not (vendor_name and email and vendor_type):
		frappe.throw(_("vendor_name, email and vendor_type are required"))

	doc = frappe.get_doc({
		"doctype": "Vendor Onboarding Request",
		"vendor_name": vendor_name,
		"email": email,
		"workflow_state": "Draft",
		"vendor_type": vendor_type,
		"contact_person": kwargs.get("contact_person"),
		"phone": kwargs.get("phone"),
		"gst_number": kwargs.get("gst_number"),
		"annual_turnover": kwargs.get("annual_turnover"),
		"documents_submitted": cint(kwargs.get("documents_submitted", 0)),
	})

	doc.insert()
	return doc.name

@frappe.whitelist(methods=["GET"])
def get_request(name):
	if not frappe.db.exists("Vendor Onboarding Request", name):
		frappe.throw(_("Vendor Onboarding Request {0} not found").format(name), frappe.DoesNotExistError)

	doc = frappe.get_doc("Vendor Onboarding Request", name)

	return {
		"name": doc.name,
		"vendor_name": doc.vendor_name,
		"status": doc.workflow_state,
	}