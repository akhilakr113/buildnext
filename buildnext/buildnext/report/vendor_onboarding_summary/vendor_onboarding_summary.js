// Copyright (c) 2026, akhila and contributors
// For license information, please see license.txt

frappe.query_reports["Vendor Onboarding Summary"] = {
	filters: [
		{
			fieldname: "vendor_type",
			label: __("Vendor Type"),
			fieldtype: "Select",
			options: "\nMaterial Supplier\nContractor\nService Provider",
			default: "",
		},
	]
};
