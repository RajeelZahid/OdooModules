from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    show_detailed_constrain_err = fields.Boolean(string="Show Detailed Constrain Errors")

