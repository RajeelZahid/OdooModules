# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.exceptions import UserError
from odoo import _, api, fields, models
from odoo.addons.web.controllers.utils import get_action


def remove_search_default(ctx):
    if not ctx:
        return ctx
    return {key: value for key, value in eval(ctx).items() if not key.startswith('search_default_')}


def get_list_ids(ids):
    return list(map(int, ids.split(',')))


class SharedRecsLinkWizard(models.TransientModel):
    _name = 'shared.recs.link.wizard'
    _description = "Shared Records Link"
    _transient_max_hours = 72  # delete links after 3 days

    res_model = fields.Char()
    res_ids = fields.Text()
    action = fields.Char()
    link = fields.Char()

    def view_records(self):
        if not self.res_ids:
            raise UserError('No IDs Linked')
        if not (action := get_action(self.sudo().env, self.action)):
            raise UserError(f'Action {self.action} not found')
        action = action.read()[0]
        action['domain'] = [['id', 'in', get_list_ids(self.res_ids)]]
        action['context'] = remove_search_default(action['context'])
        return action
