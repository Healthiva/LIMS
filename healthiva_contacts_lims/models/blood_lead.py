# -*- coding: utf-8 -*-

from odoo import models, fields, api

class BloodLead(models.Model):
    _name = 'healthiva.blood_lead'

    active = fields.Boolean(default=True)
    race = fields.Selection(string="Patient Race", default='unknown', selection=[('asian', 'Asian'), ('baa', 'Black or African American'), ('an', 'American Indian/Alaska Native'), ('caucasian', 'White/Caucasian'), ('other', 'Other Race'), ('unknown', 'Unknown/Not Indicated')])
    hispanic=fields.Selection(string="Hispanic Heritage", default='unknown', selection=[('no', 'No'), ('yes', 'Yes'), ('unknown', 'Unknown')])
    blood_lead_type=fields.Selection(string="Type", selection=[('venous', 'Venous'), ('finger', 'Finger Stick'), ('urine', 'Urine')])
    purpose=fields.Selection(string="Purpose", selection=[('initial', 'Initial'), ('repeat', 'Repeat'), ('follow_up', 'Follow-Up')])
    county_code=fields.Char(string="County Code Number")
    comment=fields.Text(string="Notes")