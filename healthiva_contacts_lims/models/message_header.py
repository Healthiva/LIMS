# -*- coding: utf-8 -*-

from odoo import models, fields, api

class MessageHeader(models.Model):
    _name = 'healthiva.message_header'
    _description = "Message Header (MSH)"

    active = fields.Boolean(default=True, groups="healthiva_contacts_lims.group_contact_admin")
    field_delimiter=fields.Char(string="Field Delimiter")
    component_delimiter=fields.Char(string="Component Delimiter")
    sending_application=fields.Char(string="Sending Application")
    sending_facility=fields.Char(string="Sending Facility")
    receiving_application=fields.Char(string="Receiving Application")
    receiving_facility=fields.Char(string="Receiving Facility")
    receive_date=fields.Char(string="Receiving Date/Time of Message")
    security=fields.Char(string="Security")
    message_type=fields.Char(string="Message Type")
    message_controlid=fields.Char(string="Message Control ID")
    processingid=fields.Char(string="Processing ID")
    hl7_version=fields.Char(string="Version of HL7")
    patient_id = fields.Many2one("res.partner", string="Patient")