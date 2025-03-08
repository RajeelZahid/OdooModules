from odoo import models, api, _
from psycopg2.errors import IntegrityError


def modify_exception_and_raise(obj, exc, method, vals):
    if obj.env.company.show_detailed_constrain_err:
        if not hasattr(exc, 'show_detail'):  # handle because the error cause can be from one2many fields and details already picked up
            exc.show_detail = True
            exc.vals = vals
            exc.cause_method = method
            exc.rec_name = ''
            if method == 'write':
                if len(obj) == 1 and (hasattr(obj, 'name') or hasattr(obj, 'display_name')):
                    exc.rec_name += f'{(obj.name or obj.display_name)} ({obj._name}{obj._ids})'
                exc.rec_name = f'{obj._name}{obj._ids}'
            else:
                exc.rec_name += f'{obj._name}'
    raise exc


class Model(models.AbstractModel):
    _inherit = 'base'

    @api.model
    def _create(self, data_list):
        try:
            return super(Model, self)._create(data_list)
        except IntegrityError as exc:
            modify_exception_and_raise(self, exc, 'create', [v['stored'] for v in data_list])
        except Exception:
            raise

    def _write_multi(self, vals_list):
        try:
            return super(Model, self)._write_multi(vals_list)
        except IntegrityError as exc:
            modify_exception_and_raise(self, exc, 'write', vals_list)
        except Exception:
            raise
