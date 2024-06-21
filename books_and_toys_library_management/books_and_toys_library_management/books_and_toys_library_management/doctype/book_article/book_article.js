// Copyright (c) 2024, Lakshyajeet Singh Goyal and contributors
// For license information, please see license.txt

frappe.ui.form.on('Book Article', {
	total_quantity(frm) {
		cur_frm.set_value('stock', frm.doc.total_quantity);
	}
});
