from odoo import fields, models, api, _
from odoo.exceptions import UserError


class access_management(models.Model):
    _name = 'access.management'
    _description = "Access Management"

    name = fields.Char('Name')
    user_ids = fields.Many2many('res.users', 'access_management_users_rel_ah', 'access_management_id', 'user_id', 'Users')

    readonly = fields.Boolean('Read-Only')
    active = fields.Boolean('Active',default=True)

    hide_menu_ids = fields.Many2many('ir.ui.menu', 'access_management_menu_rel_ah', 'access_management_id', 'menu_id', 'Hide Menu')
    
    hide_field_ids = fields.One2many('hide.field', 'access_management_id', 'Hide Field', copy=True)

    remove_action_ids = fields.One2many('remove.action', 'access_management_id', 'Remove Action', copy=True)

    access_domain_ah_ids = fields.One2many('access.domain.ah','access_management_id','Access Domain', copy=True)
    hide_view_nodes_ids = fields.One2many('hide.view.nodes','access_management_id','Button/Tab Access', copy=True)

    self_module_menu_ids = fields.Many2many('ir.ui.menu','access_management_ir_ui_self_module_menu','access_management_id','menu_id','Self Module Menu',compute="_get_self_module_info")
    self_model_ids = fields.Many2many('ir.model','access_management_ir_model_self','access_management_id','model_id','Self Model',compute="_get_self_module_info")
    total_rules = fields.Integer('Access Rules',compute="_count_total_rules")

    hide_chatter = fields.Boolean('Hide Chatter')
    disable_debug_mode = fields.Boolean('Disable Developer Mode')

    company_ids = fields.Many2many('res.company', 'access_management_comapnay_rel', 'access_management_id', 'company_id', 'Companies', required=True, default=lambda self: self.env.company)

    hide_filters_groups_ids = fields.One2many('hide.filters.groups','access_management_id','Hide Filters/Group By', copy=True)

    def _count_total_rules(self):
        for rec in self:
            rule = 0
            rule = rule + len(rec.hide_menu_ids) + len(rec.hide_field_ids) + len(rec.remove_action_ids) + len(rec.access_domain_ah_ids) + len(rec.hide_view_nodes_ids)
            rec.total_rules = rule

    def action_show_rules(self):
        pass

    def _get_self_module_info(self):
        access_menu_id = self.env.ref('simplify_access_management.main_menu_simplify_access_management')
        model_list = ['access.management','access.domain.ah','action.data','hide.field','hide.view.nodes','store.model.nodes','remove.action','view.data']
        models_ids = self.env['ir.model'].search([('model','in',model_list)])
        for rec in self:
            rec.self_module_menu_ids = False
            rec.self_model_ids = False
            if access_menu_id:
                rec.self_module_menu_ids = [(6,0,access_menu_id.ids)]
            if models_ids:
                rec.self_model_ids = [(6,0,models_ids.ids)]


    def toggle_active_value(self):
        for record in self:
            record.write({'active' : not record.active})
        return True                

    # @api.model_create_multi
    @api.model
    def create(self, vals_list):
        res = super(access_management, self).create(vals_list)
        # for user in self.env['res.users'].sudo().search([('share','=',False)]):
            # user.clear_caches()
        self.clear_caches()
        for record in res:
            if record.readonly:
                for user in record.user_ids:
                    if user.has_group('base.group_system') or user.has_group('base.group_erp_manager'):
                        raise UserError(_('Admin user can not be set as a read-only..!'))
        return res

    def unlink(self):
        res = super(access_management, self).unlink()
        self.clear_caches()
        # for user in self.env['res.users'].sudo().search([('share','=',False)]):
        #     user.clear_caches()
        return res

    def write(self, vals):
        res = super(access_management, self).write(vals)
        
        if self.readonly:
            for user in self.user_ids:
                if user.has_group('base.group_system') or user.has_group('base.group_erp_manager'):
                    raise UserError(_('Admin user can not be set as a read-only..!'))
        # for user in self.env['res.users'].sudo().search([('share','=',False)]):
        #     user.clear_caches()
        self.clear_caches()
        return res     


    def get_remove_options(self, model):
        remove_action = self.env['remove.action'].sudo().search([('access_management_id.company_ids','in',self.env.company.id),('access_management_id','in',self.env.user.access_management_ids.ids),('model_id.model','=',model)])
        options = []
        for action in remove_action:
            if action.restrict_export:
                options.append(_('Export'))
            if action.restrict_archive_unarchive:
                options.append(_('Archive'))
                options.append(_('Unarchive'))
            if action.restrict_duplicate:
                options.append(_('Duplicate'))
        return options
