# Copyright (c) 2024, Lakshyajeet Singh Goyal and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from datetime import date


class BookTransaction(Document):
    def before_submit(self):
        if self.transaction_type == "Issue":
            self.validate_issue()
            loan_period = frappe.db.get_single_value("Library Settings", "loan_period")
            self.to_date = frappe.utils.add_days(self.from_date, loan_period)
            article = frappe.get_doc("Book Article", self.title)
            article.stock -= 1
            if article.stock > 0:
                article.status = 'Available'
            elif article.stock == 0:
                article.status = 'Issued'
            article.save()

        elif self.transaction_type == "Return":
            self.validate_return()
            article = frappe.get_doc("Book Article", self.title)
            article.status = "Available"
            article.stock += 1
            article.save()
            loan_period = frappe.db.get_single_value("Library Settings", "loan_period")
            self.to_date = frappe.utils.add_days(self.from_date, loan_period)
            if date.fromisoformat(self.return_date) > date.fromisoformat(self.to_date):
                frappe.msgprint("Late Submission")

    def validate_issue(self):
        article = frappe.get_doc("Book Article", self.title)
        transaction_type = frappe.db.get_value('Book Transaction', {
                "library_member": self.library_member, "title": self.title, "docstatus": 1
            }, "transaction_type")
        if article.status == "Issued":
            frappe.throw("Article is already issued to other members")
        elif transaction_type == "Issue":
            frappe.throw("Article is already issued to this member")

    def validate_return(self):
        article = frappe.get_doc("Book Article", self.title)
        transaction_type = frappe.db.get_value('Book Transaction', {
                "library_member": self.library_member, "title": self.title, "docstatus": 1
            }, "transaction_type")
        if transaction_type == "Return":
            frappe.throw("Article is already returned by this member")
        elif article.stock == article.total_quantity:
            frappe.throw("Article cannot be returned without being issued first")
