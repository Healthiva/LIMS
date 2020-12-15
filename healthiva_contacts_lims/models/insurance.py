# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Insurance(models.Model):
    _name = 'healthiva.insurance'
    _inherit = ['mail.thread']
    _description = "Insurance (IN1)"

    active = fields.Boolean(default=True, groups="healthiva_contacts_lims.group_contact_admin")
    sequence_number=fields.Integer(string="Sequence Number")
    plan_id=fields.Char(string="Plan ID")
    id_number=fields.Char(string="Identification Number")
    payer_code=fields.Char(string="Payer Code")
    company_name=fields.Char(string="Company Name")
    company_address1=fields.Char(string="Company Address Line 1")
    company_address2=fields.Char(string="Company Address Line 2")
    company_address_city=fields.Char(string="Company Address City")
    company_address_state=fields.Char(string="Company Address State")
    company_address_zip=fields.Char(string="Company Address Zip Code")
    contact_name=fields.Char(string="Company Contact Name")
    phone=fields.Char(string="Phone Number")
    group_number=fields.Char(string="Group Number of Insured Patient")
    group_name=fields.Char(string="Group Name")
    employerid=fields.Char(string="Insured's Group Employer ID")
    employer_name=fields.Char(string="Insured's Group Employer Name")
    plan_effective_date=fields.Datetime(string="Plan Effective Date/Time")
    plan_expiration_date=fields.Datetime(string="Plan Expiration Date/Time")
    authorization_info=fields.Char(string="Authorization Information")
    plan_type=fields.Char(string="Plan Type")
    insured_last_name=fields.Char(string="Last Name of Insured")
    insured_first_name=fields.Char(string="First Name of Insured")
    insured_middle_name=fields.Char(string="Middle Name of Insured")
    insured_relation=fields.Char(string="Insured's Relationship to Patient")
    insured_dob=fields.Date(string="Insured's Date of Birth")
    insured_address1=fields.Char(string="Insured's Address Line 1")
    insured_address2=fields.Char(string="Insured's Address Line 2")
    insured_address_city=fields.Char(string="Insured's Address City")
    insured_address_state=fields.Char(string="Insured's Address State")
    insured_address_zip=fields.Char(string="Insured's Address Zip Code")
    assignment_benefits=fields.Char(string="Assignement of Benefits")
    coordinator_benefits=fields.Char(string="Coordinator of Benefits")
    primary_payer=fields.Char(string="Primary Payer")
    notice_admit_code=fields.Char(string="Notice of Admission Code")
    notice_admit_date=fields.Datetime(string="Notice of Admission Date/Time")
    report_eligibility_flag=fields.Char(string="Report of Eligibility Flag")
    report_eligibility_date=fields.Datetime(string="Report of Eligibility Date/Time")
    release_info_code=fields.Char(string="Release Information Code")
    preadmit_certification=fields.Char(string="Pre-admit Certification")
    verification_date=fields.Datetime(string="Verification Date/Time")
    verification_by=fields.Char(string="Verification By")
    agreement_type=fields.Char(string="Type of Agreement (Worker’s Compensation Flag)")
    bill_status=fields.Char(string="Billing Status")
    reserve_days=fields.Char(string="Lifetime Reserve Days")
    reserve_days_delay=fields.Char(string="Delay before Lifetime Reserve Days")
    company_plan_code=fields.Char(string="Company Plan Code")
    policy_number=fields.Char(string="Policy Number (Insurance Number/Subscriber Number/Member ID)")
    patient_id = fields.Many2one("res.partner", string="Patient")
    comment=fields.Text(string="Notes")

    def write(self, vals):
        initial_rec = self.read()[0]
        rslt = super(Insurance, self.sudo()).write(vals)
        final_rec = self.read()[0]
        body = "{} Updated the following fields:<br/>".format(final_rec['write_date'].strftime("%d/%m/%y %H:%M"))
        for key in initial_rec:
            if initial_rec[key] != final_rec[key] and key != 'write_date':
                body += "{} changed from {} to {}<br/>".format(self._fields[key].string, initial_rec[key], final_rec[key])
        self.message_post(body=body, author_id=self.env.user.partner_id.id)
        return rslt
