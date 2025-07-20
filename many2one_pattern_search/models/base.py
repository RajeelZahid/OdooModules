from odoo import api, fields, models
from odoo.osv import expression


def wildcard_wrap(string):
    return '%' + '%'.join(string) + '%'


class Base(models.AbstractModel):
    _inherit = 'base'

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        if self._context.get('pattern_search'):
            name = wildcard_wrap(name)
        return super(Base, self).name_search(name=name, args=args, operator=operator, limit=limit)
