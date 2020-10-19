# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Observation(models.Model):
    _name = 'healthiva.observation'
    _inherit = ['mail.thread']
    _description = "Observation (OBR)"

    active = fields.Boolean(default=True, groups="healthiva_contacts_lims.group_contact_admin")
    sequence_number=fields.Integer(string="Sequence Number")
    foreign_accessionid=fields.Char(string="Unique Foreign Accession ID")
    foreign_appid=fields.Char(string="Foreign Application Institution ID")
    internal_accessionid=fields.Char(string="Internal Accession ID")
    internal_appid=fields.Char(string="Internal Application Institution ID")
    battery_identifier=fields.Char(string="Observation Battery Identifier")
    battery_text=fields.Char(string="Observation Battery Text")
    coding_system1=fields.Char(string="Name of Coding System")
    priority=fields.Char(string="Priority")
    specimen_collect_date=fields.Char(string="Speciment Collection Date/Time")
    specimen_collect_end_time=fields.Char(string="Speciment Collection End Time")
    collection_volume=fields.Float(string="Collection/Urine Volume")
    collection_uom=fields.Char(string="Collection/Urine Unit of Measure")
    collector_identifier=fields.Char(string="Collector Identifier")
    action_code=fields.Char(string="Action Code")
    danger_code=fields.Char(string="Danger Code")
    clinic_info=fields.Text(string="Relevant Clinical Information")
    clinic_info_back=fields.Text(string="Relevant Clinical Information (For Backwards Compatibility")
    specimen_receipt_date=fields.Char(string="Date/Time of Specimen Receipt in Lab")
    specimen_source=fields.Char(string="Specimen Source")
    providerid=fields.Integer(string="Ordering Provider ID")
    provider_last=fields.Char(string="Ordering Provider Last Name")
    provider_first=fields.Char(string="Ordering Provider First Initial")
    provider_middle=fields.Char(string="Ordering Provider Middle Initial")
    provider_suffix=fields.Char(string="Ordering Provider Suffix")
    provider_prefix=fields.Char(string="Ordering Provider Prefix")
    provider_degree=fields.Char(string="Ordering Provider Degree")
    source_table = fields.Selection(string="Source Table", default="U", selection=[('U', 'Unknown'), ('N', 'NPI Number'), ('L', 'Local'), ('U', 'UPIN'), ('P', 'Provider Number')])
    phone=fields.Char(string="Order Callback Phone Number")
    alternate_foreign_accessionid=fields.Char(string="Alternate Unique Foreign Accession ID")
    requester_field2=fields.Char(string="Requester Field")
    producer_field1=fields.Char(string="Producer Field 1")
    microbiology_organism=fields.Char(string="Microbiology Organism")
    coding_system2=fields.Char(string="Name of Coding System")
    producer_field2=fields.Char(string="Producer Field 2")
    report_date=fields.Char(string="Date/Time of Observations Reported")
    producer_charge=fields.Char(string="Producer's Charge")
    producer_sectionid=fields.Char(string="Producer's Section ID")
    order_result_status = fields.Selection(string="Order Result Status:", selection=[('F', 'Final'), ('P', 'Preliminary'), ('X', 'Cancelled'), ('C', 'Corrected')])
    organism_link=fields.Char(string="Link to Parent Result or Organism Link to Susceptibility")
    subid=fields.Char(string="Sub ID")
    quantity_timing=fields.Integer(string="Quantity/Timing")
    courtesy_copies=fields.Integer(string="Courtesy Copies To")
    parent_order_link=fields.Char(string="Link to Parent Order")
    comment=fields.Text(string="Notes")
    patient_id = fields.Many2one("res.partner", string="Patient")

    def write(self, vals):
        initial_rec = self.read()[0]
        rslt = super(Observation, self.sudo()).write(vals)
        final_rec = self.read()[0]
        body = "{} Updated the following fields:<br/>".format(final_rec['write_date'].strftime("%d/%m/%y %H:%M"))
        for key in initial_rec:
            if initial_rec[key] != final_rec[key] and key != 'write_date':
                body += "{} changed from {} to {}<br/>".format(self._fields[key].string, initial_rec[key], final_rec[key])
        self.message_post(body=body, author_id=self.env.user.partner_id.id)
        return rslt
