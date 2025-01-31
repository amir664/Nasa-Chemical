from odoo import api, models, fields, _

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    powerbi_verify_token = fields.Char(string='Verify Token', config_parameter='powerbi.verify_token')

    # def set_values(self):
    #     config_parameters = self.env['ir.config_parameter'].sudo()
    #     config_parameters.set_param('powerbi.verify_token', self.powerbi_verify_token)

    # def get_values(self):
    #     config_parameters = self.env['ir.config_parameter'].sudo()
    #     config_parameters['powerbi_verify_token'] = config_parameters.get_param('powerbi.verify_token')
    #     return config_parameters