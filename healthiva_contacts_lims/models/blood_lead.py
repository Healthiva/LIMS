# -*- coding: utf-8 -*-

from odoo import models, fields, api

class BloodLead(models.Model):
    _name = 'healthiva.blood_lead'
    _inherit = ['mail.thread']
    _description = "Blood Lead (ZBL)"

    active=fields.Boolean(default=True, groups="healthiva_contacts_lims.group_contact_admin")
    race=fields.Selection(string="Patient Race", default='unknown', selection=[('asian', 'Asian'), ('baa', 'Black or African American'), ('an', 'American Indian/Alaska Native'), ('caucasian', 'White/Caucasian'), ('other', 'Other Race'), ('unknown', 'Unknown/Not Indicated')])
    hispanic=fields.Selection(string="Hispanic Heritage", default='unknown', selection=[('no', 'No'), ('yes', 'Yes'), ('unknown', 'Unknown')])
    blood_lead_type=fields.Selection(string="Type", selection=[('venous', 'Venous'), ('finger', 'Finger Stick'), ('urine', 'Urine')])
    purpose=fields.Selection(string="Purpose", selection=[('initial', 'Initial'), ('repeat', 'Repeat'), ('follow_up', 'Follow-Up')])
    county_code=fields.Char(string="County Code Number")
    patient_id = fields.Many2one("res.partner", string="Patient")
    comment=fields.Text(string="Notes")

    def write(self, vals):
        initial_rec = self.read()[0]
        rslt = super(BloodLead, self.sudo()).write(vals)
        final_rec = self.read()[0]
        body = "{} Updated the following fields:<br/>".format(final_rec['write_date'].strftime("%d/%m/%y %H:%M"))
        for key in initial_rec:
            if initial_rec[key] != final_rec[key] and key != 'write_date':
                body += "{} changed from {} to {}<br/>".format(self._fields[key].string, initial_rec[key], final_rec[key])
        self.message_post(body=body, author_id=self.env.user.partner_id.id)
        return rslt