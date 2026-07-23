from odoo import api, fields, models
from odoo.tools.translate import _

from ..services import compare_engine, connection

COMPARE_STEPS = (
    ('compare_modules', 'module', compare_engine.compare_modules),
    ('compare_models', 'model', compare_engine.compare_models),
    ('compare_fields', 'field', compare_engine.compare_fields),
    ('compare_menus', 'menu', compare_engine.compare_menus),
    ('compare_views', 'view', compare_engine.compare_views),
)


class DatabaseDiffCreate(models.TransientModel):
    _name = 'database.diff.create'
    _description = 'Create Database Diff Report'

    use_current_env_for_subject = fields.Boolean(string='Use Current Environment', default=True)
    subject_url = fields.Char(string='URL')
    subject_db = fields.Char(string='Database')
    subject_username = fields.Char(string='Username')
    subject_password = fields.Char(string='Password')

    use_current_env_for_target = fields.Boolean(string='Use Current Environment')
    target_url = fields.Char(string='URL')
    target_db = fields.Char(string='Database')
    target_username = fields.Char(string='Username')
    target_password = fields.Char(string='Password')

    compare_modules = fields.Boolean(default=True)
    compare_models = fields.Boolean(default=True)
    compare_fields = fields.Boolean(default=True)
    compare_menus = fields.Boolean(default=True)
    compare_views = fields.Boolean(default=True)

    @api.onchange('use_current_env_for_subject')
    def _onchange_use_current_env_for_subject(self):
        if self.use_current_env_for_subject:
            self.subject_db = self.env.cr.dbname

    @api.onchange('use_current_env_for_target')
    def _onchange_use_current_env_for_target(self):
        if self.use_current_env_for_target:
            self.target_db = self.env.cr.dbname

    def _build_source(self, prefix):
        return connection.get_source(
            self.env,
            use_current_env=self['use_current_env_for_%s' % prefix],
            url=self['%s_url' % prefix],
            db_name=self['%s_db' % prefix],
            username=self['%s_username' % prefix],
            password=self['%s_password' % prefix],
        )

    def action_create_report(self):
        self.ensure_one()

        subject_source = self._build_source('subject')
        target_source = self._build_source('target')

        subject_source_url = subject_source.url + '/web?db=' + subject_source.db_name
        target_source_url = target_source.url + '/web?db=' + target_source.db_name

        diff = self.env['database.diff'].sudo().create({
            'name': '%s | %s | %s' % (fields.Datetime.now(), subject_source.db_name, target_source.db_name),
            'subject_db_url': subject_source_url,
            'target_db_url': target_source_url,
        })

        counts = {}
        all_lines = []
        for flag_field, diff_type, compare_func in COMPARE_STEPS:
            if not self[flag_field]:
                counts[diff_type] = 0
                continue
            result_lines = compare_func(subject_source, target_source)
            counts[diff_type] = len(result_lines)
            all_lines.extend(result_lines)

        line_vals = []
        for index, line in enumerate(all_lines):
            line = dict(line, diff_id=diff.id, sequence=index)
            line_vals.append(line)

        if line_vals:
            self.env['database.diff.line'].sudo().create(line_vals)

        diff.sudo().write({
            'module_count': counts.get('module', 0),
            'model_count': counts.get('model', 0),
            'field_count': counts.get('field', 0),
            'menu_count': counts.get('menu', 0),
            'view_count': counts.get('view', 0),
            'total_count': sum(counts.values()),
        })

        return {
            'type': 'ir.actions.act_window',
            'name': _('Report Lines'),
            'res_model': 'database.diff.line',
            'view_mode': 'list',
            'domain': [('diff_id', '=', diff.id)],
            'context': {'default_diff_id': diff.id},
        }

    def action_cancel(self):
        return {'type': 'ir.actions.act_window_close'}
