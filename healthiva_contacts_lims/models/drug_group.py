# -*- coding: utf-8 -*-

from odoo import models, fields, api

class DrugGroup(models.Model):
    _name = 'healthiva.drug_group'
    _description = "Drug Group"


    active = fields.Boolean(default=True, groups="healthiva_contacts_lims.group_contact_admin")
    name = fields.Char(string="Name")