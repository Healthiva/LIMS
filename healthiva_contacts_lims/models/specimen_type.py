# -*- coding: utf-8 -*-

from odoo import models, fields, api

class SpecimenType(models.Model):
    _name = 'healthiva.specimen_type'
    _description = "Specimen Type"

    active = fields.Boolean(default=True, groups="healthiva_contacts_lims.group_contact_admin")
    name = fields.Char(string="Name")