# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Insurance(models.Model):
    _name = 'healthiva.guarantor'

    active = fields.Boolean(default=True)
    first_name=fields.Char(string="Guarantor First Name")
    middle_name=fields.Char(string="Guarantor Middle Name")
    last_name=fields.Char(string="Guarantor Last Name")
    spouse_name=fields.Char(string="Spouse Name")
    dob=fields.Date(string="Guarantor DOB")
    guarantor_type=fields.Char(string="Guarantor Type")
    patient_relation=fields.Char(string="Guarantor Relationship to Patient")
    ssn=fields.Char(string="Guarantor ID Number")
    begin_date=fields.Datetime(string="Guarantor Date/Time - Begin")
    end_date=fields.Datetime(string="Guarantor Date/Time - End")
    priority=fields.Char(string="Guarantor Priority")
    employer_name=fields.Char(string="Guarantor Employer Name")
    comment=fields.Text(string="Notes")