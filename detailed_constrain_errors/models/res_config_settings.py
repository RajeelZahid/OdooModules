from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    show_detailed_constrain_err = fields.Boolean(related='company_id.show_detailed_constrain_err',
                                                 string="Show Detailed Constrain Errors", readonly=False)
