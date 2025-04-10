from odoo import models, fields,api
from odoo.tools.safe_eval import safe_eval
import logging

_logger = logging.getLogger(__name__)

class MyModelMain(models.Model):
    _name = 'my.model.main'
    _description = 'Main Form Model'

    name = fields.Char(string='Name')
    user_ids = fields.Many2many('res.users', string="Users")
    line_ids = fields.One2many('my.model.line', 'main_id', string='Model Lines')
    custom_model_id = fields.Many2one('ir.model', string='Model')
    model_name = fields.Char(related="custom_model_id.model",string="Model Name")

    def check_notification(self, record):
        for rule in self:
            for line in rule.line_ids:
                try:
                    local_dict = {'record': record}
                    raise UserError(str(local_dict))
                    if safe_eval(line.condition, local_dict):
                        message = line.message.format(record=record)
                        record.message_post(
                            body=message,
                            partner_ids=rule.user_ids.mapped('partner_id').ids,
                            subtype_xmlid="mail.mt_comment"
                        )
                except Exception as e:
                    _logger.error("Failed condition eval: %s", e)


    
class MyModelLine(models.Model):
    _name = 'my.model.line'
    _description = 'Lines for Models and Fields'

    main_id = fields.Many2one('my.model.main', string='Main Record')    
    condition = fields.Char(string="Condition", help="Use Python syntax. Ex: record.amount_total > 1000")
    message_template = fields.Text(string="Message Template", help="Use ${record.field_name} to include values dynamically.")

    # @api.model
    # def check_and_notify(self, model_name, record):
    #     rules = self.search([]).filtered(lambda r: r.main_id.model_name == model_name)
    #     for rule in rules:
    #         try:
    #             local_dict = {'record': record}
    #             if safe_eval(rule.condition, local_dict):
    #                 msg = rule.message_template
    #                 try:
    #                     msg = msg.format(record=record)
    #                 except Exception as format_err:
    #                     _logger.warning("Failed to format message: %s", format_err)
    #                 record.message_post(
    #                     body=msg,
    #                     partner_ids=rule.rule_id.user_ids.mapped('partner_id').ids,
    #                     subtype_xmlid="mail.mt_comment"
    #                 )
    #         except Exception as e:
    #             _logger.error("Failed to evaluate condition: %s", e)