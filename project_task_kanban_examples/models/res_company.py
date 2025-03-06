from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    more_project_kanban_examples = fields.Boolean(string="Show More Kanban Examples")

