from odoo import models, fields, api
from odoo.http import request
from odoo.exceptions import AccessDenied


class IrView(models.Model):
    _inherit = 'ir.ui.view'

    old_groups_id = fields.Many2many('res.groups', 'ir_ui_view_group_old_rel', 'view_id', 'group_id')
