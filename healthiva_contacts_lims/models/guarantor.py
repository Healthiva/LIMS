# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Guarantor(models.Model):
    _name = 'healthiva.guarantor'
    _inherit = ['mail.thread']
    _description = "Guarantor (GT1)"

    active = fields.Boolean(default=True, groups="healthiva_contacts_lims.group_contact_admin")
    sequence_number=fields.Integer(string="Sequence Number")
    guarantor_number=fields.Char(string="Guarantor Number")
    last_name=fields.Char(string="Guarantor Last Name")
    first_name=fields.Char(string="Guarantor First Name")
    middle_name=fields.Char(string="Guarantor Middle Initial")
    spouse_name=fields.Char(string="Spouse Name")
    guarantor_address1=fields.Char(string="Guarantor Address Line 1")
    guarantor_address2=fields.Char(string="Guarantor Address Line 2")
    guarantor_address_city=fields.Char(string="Guarantor Address City")
    guarantor_address_state=fields.Char(string="Guarantor Address State")
    guarantor_address_zip=fields.Char(string="Guarantor Address Zip Code")
    phone=fields.Char(string="Guarantor Phone Number")
    work_phone=fields.Char(string="Guarantor Work Phone Number")
    dob=fields.Char(string="Guarantor DOB")
    gender=fields.Char(string="Guarantor Gender")
    guarantor_type=fields.Char(string="Guarantor Type")
    patient_relation=fields.Selection(string="Guarantor Relationship to Patient", default='U', selection=[('U', 'Unknown'), ('1', 'Self'), ('2', 'Spouse'), ('3', 'Other')])
    ssn=fields.Char(string="Guarantor ID Number")
    begin_date=fields.Char(string="Guarantor Date/Time - Begin")
    end_date=fields.Char(string="Guarantor Date/Time - End")
    priority=fields.Char(string="Guarantor Priority")
    employer_name=fields.Char(string="Guarantor Employer Name")
    patient_id = fields.Many2one("res.partner", string="Patient")
    comment=fields.Text(string="Notes")

    def write(self, vals):
        initial_rec = self.read()[0]
        rslt = super(Guarantor, self.sudo()).write(vals)
        final_rec = self.read()[0]
        body = "{} Updated the following fields:<br/>".format(final_rec['write_date'].strftime("%d/%m/%y %H:%M"))
        for key in initial_rec:
            if initial_rec[key] != final_rec[key] and key != 'write_date':
                body += "{} changed from {} to {}<br/>".format(self._fields[key].string, initial_rec[key], final_rec[key])
        self.message_post(body=body, author_id=self.env.user.partner_id.id)
        return rslt