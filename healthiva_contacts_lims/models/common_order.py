# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CommonOrder(models.Model):
    _name = 'healthiva.common_order'
    _inherit = ['mail.thread']
    _description = "Common Order (ORC)"

    active = fields.Boolean(default=True, groups="healthiva_contacts_lims.group_contact_admin")
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
    transaction_date = fields.Char(string="Date/Time of Transaction")
    entered1 = fields.Char(string="Entered By 1")
    entered2 = fields.Char(string="Entered By 2")
    providerid = fields.Char(string="Ordering Provider ID Number")
    provider_last = fields.Char(string="Ordering Provider Last Name")
    provider_first = fields.Char(string="Ordering Provider First Initial")
    provider_middle = fields.Char(string="Ordering Provider Middle Initial")
    provider_suffix = fields.Char(string="Ordering Provider Suffix")
    provider_prefix = fields.Char(string="Ordering Provider Prefix")
    provider_degree = fields.Char(string="Ordering Provider Degree")
    source_table = fields.Selection(string="Source Table", selection=[('N', 'NPI Number'), ('L', 'Local'), ('U', 'UPIN'), ('P', 'Provider Number')])
    enterer_location = fields.Char(string="Enterer's Location")
    phone = fields.Char(string="Callback Phone Number")
    patient_id = fields.Many2one("res.partner", string="Patient")
    comment=fields.Text(string="Notes")

    def write(self, vals):
        initial_rec = self.read()[0]
        rslt = super(CommonOrder, self.sudo()).write(vals)
        final_rec = self.read()[0]
        body = "{} Updated the following fields:<br/>".format(final_rec['write_date'].strftime("%d/%m/%y %H:%M"))
        for key in initial_rec:
            if initial_rec[key] != final_rec[key] and key != 'write_date':
                body += "{} changed from {} to {}<br/>".format(self._fields[key].string, initial_rec[key], final_rec[key])
        self.message_post(body=body, author_id=self.env.user.partner_id.id)
        return rslt