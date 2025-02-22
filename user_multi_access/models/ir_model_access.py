from odoo import models, fields, api
from odoo.http import request
from odoo.exceptions import AccessDenied


class IrModelAccess(models.Model):
    _inherit = 'ir.model.access'

    from_internal = fields.Boolean()
