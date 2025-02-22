from odoo import models, fields, api
from odoo.http import request
from odoo.exceptions import AccessDenied


class IrRule(models.Model):
    _inherit = 'ir.rule'

    old_groups = fields.Many2many('res.groups', 'rule_group_old_rel', 'rule_group_id', 'group_id')
    force_inactive = fields.Boolean()