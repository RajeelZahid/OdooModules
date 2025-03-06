from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    more_project_kanban_examples = fields.Boolean(related='company_id.more_project_kanban_examples',
                                                  string="Show More Kanban Examples", readonly=False)
