// Copyright (c) 2024, Lakshyajeet Singh Goyal and contributors
// For license information, please see license.txt

frappe.ui.form.on('Library Member', {
    refresh: function(frm) {
        frm.add_custom_button('Create Transaction', () => {
            frappe.new_doc('Library Transaction', {
                library_member: frm.doc.name
            })
        })
    }
});
