from odoo import models, fields, api
from odoo.http import request
from odoo.exceptions import AccessDenied


class IrMenu(models.Model):
    _inherit = 'ir.ui.menu'

    old_groups_id = fields.Many2many('res.groups', 'ir_ui_menu_group_old_rel', 'menu_id', 'gid')
