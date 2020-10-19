# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CourtesyCopy(models.Model):
    _name = 'healthiva.courtesy'
    _inherit = ['mail.thread']
    _description = "Courtesy Copy (ZCC)"

    active = fields.Boolean(default=True, groups="healthiva_contacts_lims.group_contact_admin")
    copy_type = fields.Char(string="Type")
    copy_context = fields.Char(string="Text")
    attn_line = fields.Char(string="Attention Line")
    patient_id = fields.Many2one("res.partner", string="Patient")
    comment=fields.Text(string="Notes")

    def write(self, vals):
        initial_rec = self.read()[0]
        rslt = super(CourtesyCopy, self.sudo()).write(vals)
        final_rec = self.read()[0]
        body = "{} Updated the following fields:<br/>".format(final_rec['write_date'].strftime("%d/%m/%y %H:%M"))
        for key in initial_rec:
            if initial_rec[key] != final_rec[key] and key != 'write_date':
                body += "{} changed from {} to {}<br/>".format(self._fields[key].string, initial_rec[key], final_rec[key])
        self.message_post(body=body, author_id=self.env.user.partner_id.id)
        return rslt