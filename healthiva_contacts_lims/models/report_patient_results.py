# -*- coding: utf-8 -*-

from odoo import models, fields, api

class PatientResultsReport(models.AbstractModel):
    _name = 'report.healthiva_contacts_lims.report_patientresults'
    _description = 'Patient Results Report'

    def _get_report_values(self, docids, data=None):
        docs = self.env['healthiva.observation'].browse(docids)
        try:
            result_id = self.env['healthiva.result'].browse(docs[0].result_ids[0].id)
        except:
            result_id = None
        config = self.env['ir.config_parameter'].sudo()
        return {
            'doc_ids': docs.ids,
            'doc_model': 'healthiva.observation',
            'docs': docs,
            'result_sample': result_id,
            'config': config,
        }