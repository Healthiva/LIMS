# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Diagnosis(models.Model):
    _name = 'healthiva.diagnosis'
    _inherit = ['mail.thread']
    _description = "Diagnosis (DG1)"

    active = fields.Boolean(default=True, groups="healthiva_contacts_lims.group_contact_admin")
    sequence_number=fields.Integer(string="Sequence Number")
    code_method=fields.Char(string="Code Method")
    code_identifier=fields.Char(string="Code Identifier")
    code_text=fields.Text(string="Code Text Description")
    code_system=fields.Char(string="Name of Coding System")
    patient_id = fields.Many2one("res.partner", string="Patient")
    comment=fields.Text(string="Notes")

    def write(self, vals):
        initial_rec = self.read()[0]
        rslt = super(Diagnosis, self.sudo()).write(vals)
        final_rec = self.read()[0]
        body = "{} Updated the following fields:<br/>".format(final_rec['write_date'].strftime("%d/%m/%y %H:%M"))
        for key in initial_rec:
            if initial_rec[key] != final_rec[key] and key != 'write_date':
                body += "{} changed from {} to {}<br/>".format(self._fields[key].string, initial_rec[key], final_rec[key])
        self.message_post(body=body, author_id=self.env.user.partner_id.id)
        return rslt