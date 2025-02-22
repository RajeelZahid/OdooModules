from odoo import models, fields, api
from odoo.http import request
from odoo.exceptions import AccessDenied


class IrActWindows(models.Model):
    _inherit = 'ir.actions.act_window'

    old_groups_id = fields.Many2many('res.groups', 'ir_act_window_group_old_rel', 'act_id', 'gid')
