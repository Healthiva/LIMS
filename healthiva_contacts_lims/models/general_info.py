# -*- coding: utf-8 -*-

from odoo import models, fields, api

class GeneralInfo(models.Model):
    _name = 'healthiva.general_info'
    _inherit = ['mail.thread']
    _description = "General Information (ZCI)"

    active = fields.Boolean(default=True, groups="healthiva_contacts_lims.group_contact_admin")
    height=fields.Float(string="Height")
    weight_lb=fields.Float(string="Weight")
    weight_oz=fields.Float(string="Weight")
    weight_uom=fields.Char(string="Weight unit of measure")
    collection_volume=fields.Float(string="Collection Volume Quantity")
    collection_uom=fields.Char(string="Collection Volume Unit of Measure")
    fasting=fields.Char(string="Fasting")
    waist=fields.Float(string="Waist Measurement")
    bp_systolic=fields.Float(string="Blood Pressure Systolic")
    bp_diastolic=fields.Float(string="Blood Pressure Diastolic")
    pulse=fields.Float(string="Pulse")
    email=fields.Char(string="Patient Email")
    patient_id = fields.Many2one("res.partner", string="Patient")
    comment=fields.Text(string="Notes")

    def write(self, vals):
        initial_rec = self.read()[0]
        rslt = super(GeneralInfo, self.sudo()).write(vals)
        final_rec = self.read()[0]
        body = "{} Updated the following fields:<br/>".format(final_rec['write_date'].strftime("%d/%m/%y %H:%M"))
        for key in initial_rec:
            if initial_rec[key] != final_rec[key] and key != 'write_date':
                body += "{} changed from {} to {}<br/>".format(self._fields[key].string, initial_rec[key], final_rec[key])
        self.message_post(body=body, author_id=self.env.user.partner_id.id)
        return rslt