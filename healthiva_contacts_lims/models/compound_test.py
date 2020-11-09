# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CompoundTest(models.Model):
    _name = 'healthiva.compound_test'
    _description = "Compound Test"

    active = fields.Boolean(default=True, groups="healthiva_contacts_lims.group_contact_admin")
    name = fields.Char(string="Name")
    drug_group_id = fields.Many2one("healthiva.drug_group", required=True, string="Drug Classification")
    specimen_type_id = fields.Many2one("healthiva.specimen_type", string="Specimen Type")
    upper_limit = fields.Float(default=0, digits=(12,0), string="Upper Limit")
    detection = fields.Char(string="Detection")
    process_location_id = fields.Many2one("healthiva.process_location", string="Processing Location")
    cutoff = fields.Float(default=0, digits=(12,0), string="Cutoff")
    uom_id = fields.Many2one("uom.uom", string="Units")
    minimum_range = fields.Float(default=0, digits=(12,0), string="Minimum Range")
    maximum_range = fields.Float(default=0, digits=(12,0), string="Maximum Range")