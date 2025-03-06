from odoo import models, fields, api, _
from markupsafe import Markup


class ProjectTaskType(models.Model):
    _inherit = 'project.task.type'

    def _filter_unfold(self):
        return self.filtered(lambda s: not s.fold)

    def _filter_fold(self):
        return self.filtered(lambda s: s.fold)
