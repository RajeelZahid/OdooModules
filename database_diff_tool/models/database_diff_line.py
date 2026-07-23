from odoo import fields, models


class DatabaseDiffLine(models.Model):
    _name = 'database.diff.line'
    _description = 'Database Difference Report Line'
    _order = 'sequence, id'

    diff_id = fields.Many2one('database.diff', required=True, ondelete='cascade', readonly=True)
    sequence = fields.Integer(default=10, readonly=True)
    type = fields.Selection([
        ('module', 'Module'),
        ('model', 'Model'),
        ('field', 'Field'),
        ('menu', 'Menu'),
        ('view', 'View'),
    ], required=True, readonly=True)
    record_name = fields.Char(required=True, readonly=True)
    subject_db_record_id = fields.Integer('Subject DB Rec ID', readonly=True)
    target_db_record_id = fields.Integer('Target DB Rec ID', readonly=True)
    remarks = fields.Html(readonly=True, sanitize=False)
    remarks_plain_text = fields.Text(readonly=True)
    severity = fields.Selection([
        ('info', 'Info'),
        ('warning', 'Warning'),
        ('critical', 'Critical'),
    ], required=True, default='info', readonly=True)
