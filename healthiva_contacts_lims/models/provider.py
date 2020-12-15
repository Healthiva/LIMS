# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Provider(models.Model):
    _name = 'healthiva.provider'
    _inherit = ['mail.thread']
    _description = "Provider (PV1)"

    active = fields.Boolean(default=True, groups="healthiva_contacts_lims.group_contact_admin")
    sequence_number=fields.Integer(string="Sequence Number")
    patient_class=fields.Selection(string="Patient Class", default='U', selection=[('U', 'Unknown'), ('C', 'Commercial Account'), ('B', 'Obstetrics'), ('I', 'Inpatient'), ('O', 'Outpatient'), ('P', 'Preadmit'), ('R', 'Recurring Patient'), ('I', 'Inpatient'), ('E', 'Emergency')])
    assigned_location=fields.Char(string="Assigned Patient Location")
    admission_type=fields.Char(string="Admission Type")
    preadmit_number=fields.Char(string="Preadmit Number")
    prior_location=fields.Char(string="Prior Patient Location")
    attending_doctor_npi=fields.Char(string="Attending Doctor NPI")
    attending_doctor_first=fields.Char(string="Attending Doctor First")
    attending_doctor_last=fields.Char(string="Attending Doctor Last")
    referring_doctor=fields.Char(string="Referring Doctor")
    consulting_doctor=fields.Char(string="Consulting Doctor")
    hospital_service=fields.Char(string="Hospital Service")
    temp_location=fields.Char(string="Temporary Location")
    pretest_indicator=fields.Char(string="Preadmit Test Indicator")
    readmission=fields.Char(string="Re-admission Indicator")
    admit_source=fields.Char(string="Admit Source")
    ambulatory_status=fields.Char(string="Ambulatory Status")
    vip_indicator=fields.Char(string="VIP Indicator")
    admitting_doctor=fields.Char(string="Admitting Doctor")
    patient_type=fields.Char(string="Patient Type")
    visit_number=fields.Char(string="Visit Number")
    financial_class=fields.Char(string="Financial Class")
    charge_indicator=fields.Char(string="Charge Price Indicator")
    courtesy_code=fields.Char(string="Courtesy Code")
    credit_rating=fields.Char(string="Credit Rating")
    contract_code=fields.Char(string="Contract Code")
    contract_date=fields.Date(string="Contract Effective Date")
    contract_total=fields.Char(string="Contract Amount")
    contract_period=fields.Char(string="Contract Period")
    interest_code=fields.Char(string="Interest Code")
    tbd_code=fields.Char(string="Transfer to Bad Debt Code")
    tbd_date=fields.Date(string="Transfer to bad Debt Date")
    bda_code=fields.Char(string="Bad Debt Agency Code")
    bd_transfer_total=fields.Char(string="Bad Debt Transfer Amount")
    bd_recovery_total=fields.Char(string="Bad Debt Recovery Amount")
    delete_indicator=fields.Char(string="Delete Account Indicator")
    delete_date=fields.Date(string="Delete Account Date")
    discharge_disposition=fields.Char(string="Discharge Disposition")
    discharge_location=fields.Char(string="Discharged to Location")
    diet_type=fields.Char(string="Diet Type")
    service_location=fields.Char(string="Servicing Facility")
    bed_status=fields.Char(string="Bed Status")
    account_status=fields.Char(string="Account Status")
    pending_loc=fields.Char(string="Pending Location")
    prior_temp_location=fields.Char(string="Prior Temporary Location")
    admit_date=fields.Datetime(string="Admit Date/Time")
    discharge_date=fields.Datetime(string="Discharge Date/Time")
    current_balance=fields.Char(string="Current Patient Balance")
    charges_total=fields.Char(string="Total Charges")
    adjustments_total=fields.Char(string="Total Adjustments")
    payments_total=fields.Char(string="Total Payments")
    alt_visitid=fields.Char(string="Alternate Visit ID")
    visit_indicator=fields.Char(string="Visit Indicator")
    other_provider=fields.Char(string="Other Healthcare Provider")
    patient_id = fields.Many2one("res.partner", string="Patient")
    comment=fields.Text(string="Notes")

    def write(self, vals):
        initial_rec = self.read()[0]
        rslt = super(Provider, self.sudo()).write(vals)
        final_rec = self.read()[0]
        body = "{} Updated the following fields:<br/>".format(final_rec['write_date'].strftime("%d/%m/%y %H:%M"))
        for key in initial_rec:
            if initial_rec[key] != final_rec[key] and key != 'write_date':
                body += "{} changed from {} to {}<br/>".format(self._fields[key].string, initial_rec[key], final_rec[key])
        self.message_post(body=body, author_id=self.env.user.partner_id.id)
        return rslt
    