from odoo import models, fields,api
from odoo.tools.safe_eval import safe_eval
from odoo.exceptions import UserError
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

    def check_notification(self, record, mode=None, write_count=None):
        for rule in self:
            for line in rule.line_ids:
                if (mode == 'create' and not line.on_create) or \
                   (mode == 'write' and not line.on_write):
                    continue
                if mode == 'write' and line.times and int(line.times) != write_count:
                    continue
                try:
                    local_dict = {'record': record}
                    if safe_eval(line.condition, local_dict):
                        message = line.message_template.format(record=record)
                        record.message_post(
                            body=message,
                            partner_ids=rule.user_ids.mapped('partner_id').ids,
                            subtype_xmlid="mail.mt_comment"
                        )
                except Exception as e:
                    _logger.error("Failed to evaluate condition or send message: %s", e)
    
class MyModelLine(models.Model):
    _name = 'my.model.line'
    _description = 'Lines for Models and Fields'

    main_id = fields.Many2one('my.model.main', string='Main Record')    
    condition = fields.Char(string="Condition", help="Use Python syntax. Ex: record.amount_total > 1000")
    message_template = fields.Text(string="Message Template", help="Use ${record.field_name} to include values dynamically.")
    on_create = fields.Boolean(string="Create")
    on_write = fields.Boolean(string="Write")
    times = fields.Selection([('1','1'),('2','2'),('5','5')],string="How Many Times")


class NotificationAbstract(models.AbstractModel):
    _name = 'notification.abstract'
    _description = 'Notification Abstract'

    def _get_write_count_key(self, record):
        return f"{record._name}-{record.id}-write_count"

    def _increment_write_count(self, record):
        key = self._get_write_count_key(record)
        count = self.env.context.get(key, 0) + 1
        self.env.context = dict(self.env.context, **{key: count})
        return count

    def _get_write_count(self, record):
        key = self._get_write_count_key(record)
        return self.env.context.get(key, 1)

    @api.model
    def create(self, vals):
        record = super().create(vals)
        self.env['my.model.main'].search([
            ('model_name', '=', self._name)
        ]).check_notification(record, mode='create')
        return record

    def write(self, vals):
        for rec in self:
            count = self._increment_write_count(rec)
        res = super().write(vals)
        for rec in self:
            self.env['my.model.main'].search([
                ('model_name', '=', self._name)
            ]).check_notification(rec, mode='write', write_count=self._get_write_count(rec))
        return res
    
    