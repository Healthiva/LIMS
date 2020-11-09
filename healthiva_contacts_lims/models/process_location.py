# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ProcessLocation(models.Model):
    _name = 'healthiva.process_location'
    _description = "Processing Location"

    active = fields.Boolean(default=True, groups="healthiva_contacts_lims.group_contact_admin")
    name = fields.Char(string="Name")