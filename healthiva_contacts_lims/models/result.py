# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Result(models.Model):
    _name = 'healthiva.result'
    _inherit = ['mail.thread']
    _description = "Result (OBX)"

    active = fields.Boolean(default=True, groups="healthiva_contacts_lims.group_contact_admin")
    sequence_number=fields.Char(string="Sequence Number")
    value_type=fields.Char(string="Value Type")
    observation_identifier=fields.Char(string="Observation Identifier")
    observation_text=fields.Text(string="Observation Text")
    coding_system_name1=fields.Char(string="Name of the Coding System 1")
    alternate_identifier=fields.Char(string="Alternate Identifier")
    alternate_observation_text=fields.Text(string="Alternate Obeservation Text")
    alternate_observation_system=fields.Char(string="Name of Alternate Obeservation System")
    observation_subid=fields.Char(string="Observation Sub ID")
    observation_value=fields.Char(string="Observation Value")
    data_type=fields.Char(string="Type of Data")
    data_subtype=fields.Char(string="Data Sub Type")
    encoding=fields.Char(string="Encoding or Identifier")
    data_text=fields.Text(string="Data or Text")
    coding_system=fields.Char(string="Coding System")
    identifier=fields.Char(string="Identifier")
    result_text=fields.Text(string="Text")
    coding_system_name2=fields.Char(string="Name of the Coding System 2")
    ref_ranges=fields.Char(string="Reference Ranges")
    abnormal_flags=fields.Char(string="Abnormal Flags")
    probability=fields.Char(string="Probability")
    abnormal_test_nature=fields.Char(string="Nature of Abnormal Test")
    result_status = fields.Selection(string="Observation Result Status", selection=[('P', 'Preliminary Result'), ('X', 'Procedure cannot be done'), ('C', 'Corrected Result'), ('F', 'Result Complete'), ('I', 'Incomplete')])
    ref_range_update_date=fields.Char(string="Date of last change in reference range or units")
    access_checks=fields.Char(string="User Defined Access Checks")
    observation_date=fields.Char(string="Date/Time of Obeservation")
    producerid=fields.Char(string="Producer ID")
    observer=fields.Char(string="Responsible Observer")
    observation_method=fields.Char(string="Observation Method")
    equipment_identifier=fields.Char(string="Equipment Instance Identifier")
    analysis_date=fields.Char(string="Date/Time of the analysis")
    reserver_hamorizing1=fields.Char(string="Reserver for Hamorizing")
    reserver_hamorizing2=fields.Char(string="Reserver for Hamorizing")
    reserver_hamorizing3=fields.Char(string="Reserver for Hamorizing")
    performing_names=fields.Char(string="Performing Observation Names")
    performing_address=fields.Char(string="Performing Organization Address")
    performing_director=fields.Char(string="Performing Organization Director")
    release_category=fields.Char(string="Patient Results Release Category")
    route_cause=fields.Char(string="Route Cause")
    local_process_control=fields.Char(string="Local Process Control")
    patient_id = fields.Many2one("res.partner", string="Related Patient")
    comment=fields.Text(string="Notes")
    status=fields.Selection(string="Status", readonly=True, selection=[('pos', 'Positive'), ('neg', 'Negative')])
    compound_test_id = fields.Many2one("healthiva.compound_test", string="Compound Test")
    drug_group = fields.Char(related="compound_test_id.drug_group_id.name", readonly=True, string="Drug Group")
    specimen_type_id = fields.Many2one("healthiva.specimen_type", related="observation_id.specimen_type_id", string="Specimen Type")
    observation_id = fields.Many2one("healthiva.observation", string="Observation")

    def write(self, vals):
        initial_rec = self.read()[0]
        rslt = super(Result, self.sudo()).write(vals)
        final_rec = self.read()[0]
        body = "{} Updated the following fields:<br/>".format(final_rec['write_date'].strftime("%d/%m/%y %H:%M"))
        for key in initial_rec:
            if initial_rec[key] != final_rec[key] and key != 'write_date':
                body += "{} changed from {} to {}<br/>".format(self._fields[key].string, initial_rec[key], final_rec[key])
        self.message_post(body=body, author_id=self.env.user.partner_id.id)
        return rslt

    @api.onchange('compound_test_id', 'observation_value', 'status')
    def onchange_status(self):
        for record in self:
            try:
                if float(record.observation_value) < record.compound_test_id.minimum_range or float(record.observation_value) > record.compound_test_id.maximum_range:
                    record.status = "pos"
                else:
                    record.status = "neg"
            except:
                record.status = "neg"