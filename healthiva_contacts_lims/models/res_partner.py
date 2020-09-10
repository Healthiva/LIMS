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
    first_name = fields.Char(string="First Name")
    middle_name = fields.Char(string="Middle Name")
    last_name = fields.Char(string="Last Name")
    mother_maiden = fields.Char(string="Mother's Maiden Name")
    birth_date = fields.Date(string="Date of Birth")
    age_years = fields.Integer(string="Age Years")
    age_months = fields.Integer(string="Age Months")
    age_days = fields.Integer(string="Age Days")
    gender = fields.Selection(string="Gender", default='ni', selection=[('ni', 'Not Indicated'), ('male', 'Male'), ('female', 'Female')])
    alias = fields.Char(string="Alias")
    race = fields.Selection(string="Race", default='ni', selection=[('asian', 'Asian'), ('baa', 'Black or African American'), ('hispanic', 'Hispanic'), ('an', 'American Native'), ('aj', 'Ashkenazi Jewish'), ('sj', 'Sephardic Jewish'), ('other', 'Other'), ('ni', 'Not Indicated')])
    tele_use_code = fields.Char(string="Telecommunication Use Code")
    tele_equip_type = fields.Char(string="Telecommunication Equipment Type")
    tele_address = fields.Char(string="Telecommunication Address")
    use_code = fields.Char(string="Use Code")
    language = fields.Char(string="Language")
    marital_status = fields.Selection(string="Marital Status", default='ni', selection=[('single', 'Single'), ('married', 'Married'), ('divorced', 'Divorced'), ('widowed', 'Widowed'), ('ni', 'Not Indicated')])
    religion = fields.Char(string="Religion")
    account_number = fields.Char(string="Account Number")
    bill_type = fields.Char(string="Bill Type")
    abn_flag = fields.Char(string="ABN Flag")
    specimen_status = fields.Char(string="Status of Specimen")
    is_fasting = fields.Boolean(string="Is Fasting?")
    ssn = fields.Char(string="Social Security Number")
    driver_license = fields.Char(string="Driver's License")
    mother_identifier = fields.Char(string="Mother's Identifier")
    ethnic_group = fields.Selection(string="Ethinic Group", default='unknown', selection=[('unknown', 'Unknown'), ('hl', 'Hispanic or Latino'), ('nhl', 'Not Hispanic or Latino')])
    provider_ids = fields.One2many("healthiva.provider", "patient_id", string="Providers")
    insurance_ids = fields.One2many("healthiva.insurance", "patient_id", string="Insurances")
    common_order_ids = fields.One2many("healthiva.common_order", "patient_id", string="Common Orders")
    observation_ids = fields.One2many("healthiva.observation", "patient_id", string="Observations")
    result_ids = fields.One2many("healthiva.result", "patient_id", string="Results")
    message_header_ids = fields.One2many("healthiva.message_header", "patient_id", string="Message Header")

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
        
