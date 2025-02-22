from odoo import models, fields, api
from odoo.http import request
from odoo.exceptions import AccessDenied


class ResGroups(models.Model):
    _inherit = 'res.groups'

