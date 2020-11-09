from odoo import api, models, fields

class ResConfigSettings(models.TransientModel):

    _inherit = 'res.config.settings'

    lab_director = fields.Char(string="Lab Director", config_parameter='lab_director')
    cliaid = fields.Char(string="CLIA ID", config_parameter='cliaid')