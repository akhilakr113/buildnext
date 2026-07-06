import frappe
from frappe import qb
from pypika import Case
from frappe.query_builder.functions import Count, Sum

def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	return [
		{"label": "Vendor Type", "fieldname": "vendor_type", "fieldtype": "Data", "width": 200},
		{"label": "Total Requests", "fieldname": "total", "fieldtype": "Int", "width": 130},
		{"label": "Approved", "fieldname": "approved", "fieldtype": "Int", "width": 110},
		{"label": "Rejected", "fieldname": "rejected", "fieldtype": "Int", "width": 110},
		{"label": "Pending Review", "fieldname": "pending", "fieldtype": "Int", "width": 130},
	]


def get_data(filters=None):
	filters = filters or {}
	vor = qb.DocType("Vendor Onboarding Request")

	query = (
		qb.from_(vor)
		.select(
			vor.vendor_type,
			Count("*").as_("total"),
			Sum(Case().when(vor.workflow_state == "Approved", 1).else_(0)).as_("approved"),
			Sum(Case().when(vor.workflow_state == "Rejected", 1).else_(0)).as_("rejected"),
			Sum(
				Case().when(vor.workflow_state.isin(["Submitted", "Under Review"]), 1).else_(0)
			).as_("pending"),
		)
		.groupby(vor.vendor_type)
		.orderby(vor.vendor_type)
	)

	if filters.get("vendor_type"):
		query = query.where(vor.vendor_type == filters["vendor_type"])

	return query.run(as_dict=True)