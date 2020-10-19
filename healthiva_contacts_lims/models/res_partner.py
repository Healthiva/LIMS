# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Partner(models.Model):
    _inherit = 'res.partner'

    #Old Fields Overwritten
    company_type = fields.Selection(string="Company Type", default="person", selection=[('person', 'Individual'), ('company', 'Company')])

    #New Fields    
    sequence_number=fields.Integer(string="Sequence Number")
    external_pid = fields.Char(string="External Patient ID")
    assigned_pid = fields.Char(string="Lab Assigned Patient ID")
    alternate_pid = fields.Char(string="Alternate Patient ID")
    last_name = fields.Char(string="Last Name")
    first_name = fields.Char(string="First Name")
    middle_name = fields.Char(string="Middle Name")
    mother_maiden = fields.Char(string="Mother's Maiden Name")
    birth_date = fields.Char(string="Date of Birth")
    age_years = fields.Integer(string="Age Years")
    age_months = fields.Integer(string="Age Months")
    age_days = fields.Integer(string="Age Days")
    gender = fields.Selection(string="Gender", default='X', selection=[('X', 'Not Indicated'), ('M', 'Male'), ('F', 'Female')])
    alias = fields.Char(string="Alias")
    race = fields.Selection(string="Race", default='X', selection=[('A', 'Asian'), ('B', 'Black or African American'), ('C', 'White/Caucasian'), ('H', 'Hispanic'), ('I', 'American Native'), ('J', 'Ashkenazi Jewish'), ('S', 'Sephardic Jewish'), ('O', 'Other'), ('X', 'Not Indicated')])
    patient_address1=fields.Char(string="Patient's Address Line 1")
    patient_address2=fields.Char(string="Patient's Address Line 2")
    patient_address_city=fields.Char(string="Patient's Address City")
    patient_address_state=fields.Char(string="Patient's Address State")
    patient_address_zip=fields.Char(string="Patient's Address Zip Code")
    country_code=fields.Char(string="Country Code")
    tele_use_code = fields.Char(string="Telecommunication Use Code")
    tele_equip_type = fields.Char(string="Telecommunication Equipment Type")
    tele_address = fields.Char(string="Telecommunication Address")
    work_phone = fields.Char(string="Work Phone")
    language = fields.Char(string="Language")
    marital_status = fields.Selection(string="Marital Status", default='X', selection=[('S', 'Single'), ('M', 'Married'), ('D', 'Divorced'), ('widowed', 'Widowed'), ('X', 'Not Indicated')])
    religion = fields.Char(string="Religion")
    account_number = fields.Char(string="Account Number")
    check_digit = fields.Char(string="Check Digit")
    check_digit_scheme = fields.Char(string="Check Digit Scheme")
    bill_type = fields.Char(string="Bill Type")
    abn_flag = fields.Char(string="ABN Flag")
    specimen_status = fields.Char(string="Status of Specimen")
    is_fasting = fields.Selection(string="Is Fasting?", selection=[('Y', 'Yes'), ('N', 'No')])
    ssn = fields.Char(string="Social Security Number")
    driver_license = fields.Char(string="Driver's License")
    mother_identifier = fields.Char(string="Mother's Identifier")
    ethnic_group = fields.Selection(string="Ethinic Group", default='U', selection=[('U', 'Unknown'), ('H', 'Hispanic or Latino'), ('N', 'Not Hispanic or Latino')])
    provider_ids = fields.One2many("healthiva.provider", "patient_id", string="Providers")
    insurance_ids = fields.One2many("healthiva.insurance", "patient_id", string="Insurances")
    guarantor_ids = fields.One2many("healthiva.guarantor", "patient_id", string="Guarantors")
    diagnosis_ids = fields.One2many("healthiva.diagnosis", "patient_id", string="Diagnoses")
    common_order_ids = fields.One2many("healthiva.common_order", "patient_id", string="Common Orders")
    general_info_ids = fields.One2many("healthiva.general_info", "patient_id", string="General Information")
    observation_ids = fields.One2many("healthiva.observation", "patient_id", string="Observations")
    result_ids = fields.One2many("healthiva.result", "patient_id", string="Results")
    message_header_id = fields.Many2one("healthiva.message_header", string="Message Header")

    #MSH
    field_delimiter=fields.Char(string="Field Delimiter", related="message_header_id.field_delimiter")
    component_delimiter=fields.Char(string="Component Delimiter", related="message_header_id.component_delimiter")
    sending_application=fields.Char(string="Sending Application", related="message_header_id.sending_application")
    sending_facility=fields.Char(string="Sending Facility", related="message_header_id.sending_facility")
    receiving_application=fields.Char(string="Receiving Application", related="message_header_id.receiving_application")
    receiving_facility=fields.Char(string="Receiving Facility", related="message_header_id.receiving_facility")
    receive_date=fields.Char(string="Date/Time of Message", related="message_header_id.receive_date")
    security=fields.Char(string="Security", related="message_header_id.security")
    message_type=fields.Char(string="Message Type", related="message_header_id.message_type")
    message_controlid=fields.Char(string="Message Control ID", related="message_header_id.message_controlid")
    processingid=fields.Char(string="Processing ID", related="message_header_id.processingid")
    hl7_version=fields.Char(string="Version of HL7", related="message_header_id.hl7_version")

    def write(self, vals):
        initial_rec = self.read()[0]
        rslt = super(Partner, self.sudo()).write(vals)
        final_rec = self.read()[0]
        body = "{} Updated the following fields:<br/>".format(final_rec['write_date'].strftime("%d/%m/%y %H:%M"))
        for key in initial_rec:
            if initial_rec[key] != final_rec[key] and key != 'write_date':
                body += "{} changed from {} to {}<br/>".format(self._fields[key].string, initial_rec[key], final_rec[key])
        self.message_post(body=body, author_id=self.env.user.partner_id.id)
        return rslt

    def action_view_insurance(self):
        insurances = self.mapped('insurance_ids')
        action = self.env.ref('healthiva_contacts_lims.act_res_partner_2_insurance').read()[0]
        if len(insurances) >= 1:
            action['domain'] = [('id', 'in', insurances.ids)]
        return action

    def action_view_provider(self):
        providers = self.mapped('provider_ids')
        action = self.env.ref('healthiva_contacts_lims.act_res_partner_2_provider').read()[0]
        if len(providers) >= 1:
            action['domain'] = [('id', 'in', providers.ids)]
        return action

    def action_view_common_order(self):
        common_orders = self.mapped('common_order_ids')
        action = self.env.ref('healthiva_contacts_lims.act_res_partner_2_common_order').read()[0]
        if len(common_orders) >= 1:
            action['domain'] = [('id', 'in', common_orders.ids)]
        return action
            
    def action_view_observation(self):
        observations = self.mapped('observation_ids')
        action = self.env.ref('healthiva_contacts_lims.act_res_partner_2_observation').read()[0]
        if len(observations) >= 1:
            action['domain'] = [('id', 'in', observations.ids)]
        return action
            
    def action_view_result(self):
        results = self.mapped('result_ids')
        action = self.env.ref('healthiva_contacts_lims.act_res_partner_2_result').read()[0]
        if len(results) >= 1:
            action['domain'] = [('id', 'in', results.ids)]
        return action

    def action_send_emr(self):
        action_id = self.env['edi.sync.action'].search(['doc_type_id.doc_code', '=', 'export_contact_hl7'])
        return self.env['edi.sync.action']._do_doc_sync_cron(sync_action_id=action_id)
