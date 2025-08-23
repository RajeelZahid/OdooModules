from odoo import models, api


class Base(models.AbstractModel):
    _inherit = 'base'

    @api.model
    def fields_get(self, allfields=None, attributes=None):
        res = super().fields_get(allfields=allfields, attributes=attributes)
        for fname, field in self._fields.items():
            if fname in res and hasattr(field, 'serverless_onchange') and isinstance(field.serverless_onchange, dict):
                res[fname]['serverless_onchange'] = field.serverless_onchange
        return res

    def _valid_field_parameter(self, field, name):
        return name == 'serverless_onchange' or super()._valid_field_parameter(field, name)
