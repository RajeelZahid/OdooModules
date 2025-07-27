from odoo import models, api


class IrUiView(models.Model):
    _inherit = 'ir.ui.view'

    @api.model
    def read_template(self, view_id):
        return self._read_template(view_id)
