from odoo import api, models, fields

class ResConfigSettings(models.TransientModel):

    _inherit = 'res.config.settings'

    test_enable = fields.Boolean(string="Enable Test?", config_parameter='test_enable')
    minimum = fields.Integer(string="Minimum Range", config_parameter='minimum')
    maximum = fields.Integer(string="Maximum Range", config_parameter='maximum')