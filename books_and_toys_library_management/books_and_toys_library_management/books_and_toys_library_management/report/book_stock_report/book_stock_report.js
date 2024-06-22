// Copyright (c) 2024, Lakshyajeet Singh Goyal and contributors
// For license information, please see license.txt

frappe.query_reports["Books Stock Report"] = {
	"filters": [
		{
			"label": ("Title"),
			"fieldname": "title_filter",
			"fieldtype": "Link",
			"options": "Book Article"
		}
	]
};
