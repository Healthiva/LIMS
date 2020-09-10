# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CourtesyCopy(models.Model):
    _name = 'healthiva.courtesy'

    active = fields.Boolean(default=True)
    copy_type = fields.Char(string="Type")
    copy_context = fields.Char(string="Text")
    attn_line = fields.Char(string="Attention Line")
    comment=fields.Text(string="Notes")