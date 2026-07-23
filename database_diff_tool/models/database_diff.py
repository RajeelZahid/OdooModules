from odoo import fields, models
from odoo.tools.translate import _


class DatabaseDiff(models.Model):
    _name = 'database.diff'
    _description = 'Database Difference Report'
    _order = 'create_date desc, id desc'
    _rec_name = 'name'

    name = fields.Char(required=True, readonly=True)
    subject_db_url = fields.Char('Subject DB URL', readonly=True)
    target_db_url = fields.Char('Target DB URL', readonly=True)

    module_count = fields.Integer(readonly=True)
    model_count = fields.Integer(readonly=True)
    field_count = fields.Integer(readonly=True)
    menu_count = fields.Integer(readonly=True)
    view_count = fields.Integer(readonly=True)
    total_count = fields.Integer(readonly=True)

    line_ids = fields.One2many('database.diff.line', 'diff_id', string='Lines', readonly=True)

    def action_open_lines(self):
        self.ensure_one()
        diff_type = self.env.context.get('diff_type')
        dom = [('diff_id', '=', self.id)]
        if diff_type:
            dom.append(('type', '=', diff_type))
        ctx = (not diff_type and {'group_by': 'type'}) or {}
        return {
            'type': 'ir.actions.act_window',
            'name': _('Report Lines'),
            'res_model': 'database.diff.line',
            'view_mode': 'list',
            'domain': dom,
            'context': ctx,
        }
