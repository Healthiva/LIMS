# -*- coding: utf-8 -*-

from odoo import models, fields, api

class GeneralInfo(models.Model):
    _name = 'healthiva.general_info'

    active = fields.Boolean(default=True)
    height=fields.Float(string="Height")
    weight=fields.Float(string="Weight")
    weight_uom=fields.Float(string="Weight unit of measure")
    collection_volume=fields.Float(string="Collection Volume Quantity")
    collection_uom=fields.Float(string="Collection Volume Unit of Measure")
    waist=fields.Float(string="Waist Measurement")
    bp_systolic=fields.Float(string="Blood Pressure Systolic")
    bp_diastolic=fields.Float(string="Blood Pressure Diastolic")
    pulse=fields.Float(string="Pulse")
    email=fields.Char(string="Patient Email")
    comment=fields.Text(string="Notes")