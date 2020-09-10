# -*- coding: utf-8 -*-

from odoo import models, fields, api

class MessageHeader(models.Model):
    _name = 'healthiva.message_header'

    active = fields.Boolean(default=True)
    field_delimiter=fields.Char(string="Field Delimiter")
    component_delimiter=fields.Char(string="Component Delimiter")
    sending_application=fields.Char(string="Sending Application")
    sending_facility=fields.Char(string="Sending Facility")
    receiving_application=fields.Char(string="Receiving Application")
    receiving_facility=fields.Char(string="Receiving Facility")
    receive_date=fields.Datetime(string="RDate/Time of Message")
    security=fields.Char(string="Security")
    message_type=fields.Char(string="Message Type")
    message_controlid=fields.Char(string="Message Control ID")
    processingid=fields.Char(string="Processing ID")
    hl7_version=fields.Char(string="Version of HL7")
    patient_id = fields.Many2one("res.partner", string="Patient")
