from odoo import fields, models


class IrActionsReport(models.Model):
    _inherit = 'ir.actions.report'

    open_with_another_tab = fields.Boolean()

    def _get_readable_fields(self):
        data = super()._get_readable_fields()
        data.add('open_with_another_tab')
        return data

    def report_action(self, docids, data=None, config=True):
        data = super(IrActionsReport, self).report_action(docids, data, config)
        data['id'] = self.id
        data['open_with_another_tab'] = self.open_with_another_tab
        return data
