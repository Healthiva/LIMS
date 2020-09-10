# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CourtesyCopy(models.Model):
    _name = 'healthiva.common_order'

    active = fields.Boolean(default=True)
    order_control = fields.Char(string="Order Control")
    foreign_accessionid = fields.Char(string="Unique Foreign Accession or Specimen ID or Order ID")
    applicationid = fields.Char(string="Application/Institution ID")
    filler_accessionid = fields.Char(string="Filler Accession ID")
    accession_owner = fields.Char(string="Owner of Accession")
    placer_number = fields.Char(string="Placer Group Number")
    order_status = fields.Char(string="Order status")
    response_flag = fields.Char(string="Response Flag")
    quantity_timing = fields.Char(string="Quantity/Timing")
    parent = fields.Char(string="Parent")
    transaction_date = fields.Datetime(string="Date/Time of Transaction")
    entered1 = fields.Char(string="Entered By 1")
    entered2 = fields.Char(string="Entered By 2")
    providerid = fields.Char(string="Ordering Provider ID Number")
    provider_last = fields.Char(string="Ordering Provider Last Name")
    provider_first = fields.Char(string="Ordering Provider First Initial")
    provider_middle = fields.Char(string="Ordering Provider Middle Initial")
    provider_suffix = fields.Char(string="Ordering Provider Suffix")
    provider_prefix = fields.Char(string="Ordering Provider Prefix")
    provider_degree = fields.Char(string="Ordering Provider Degree")
    source_table = fields.Selection(string="Source Table", selection=[('npi', 'NPI Number'), ('local', 'Local'), ('upin', 'UPIN'), ('local', 'Local'), ('provider_number', 'Provider Number')])
    enterer_location = fields.Char(string="Enterer's Location")
    phone = fields.Char(string="Callback Phone Number")
    patient_id = fields.Many2one("res.partner", string="Patient")
    comment=fields.Text(string="Notes")