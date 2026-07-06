from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def execute():
	create_custom_fields(
		{
			"Supplier": [
				{
					"fieldname": "vendor_request",
					"label": "Vendor Onboarding Request",
					"fieldtype": "Link",
					"insert_after": "supplier_name",
					"options": "Vendor Onboarding Request",
					"read_only": 1,
				},
				{
					"fieldname": "supplier_category",
					"label": "Supplier Category",
					"fieldtype": "Data",
					"insert_after": "supplier_type",
				},
			]
		}
	)