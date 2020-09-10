# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Diagnosis(models.Model):
    _name = 'healthiva.diagnosis'

    active = fields.Boolean(default=True)
    sequence_number=fields.Char(string="Sequence Number")
    code_method=fields.Char(string="Code Method")
    code_identifier=fields.Char(string="Code Identifier")
    code_text=fields.Text(string="Code Text Description")
    code_system=fields.Char(string="Name of Coding System")
    comment=fields.Text(string="Notes")