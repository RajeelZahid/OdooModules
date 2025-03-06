from odoo import models, fields, api, _
from markupsafe import Markup


class TaskKanbanExample(models.Model):
    _name = 'project.task.kanban.example'
    _description = 'Project Task Kanban Example'
    _order = 'sequence'

    sequence = fields.Integer()
    name = fields.Char(required=True)
    description = fields.Html()
    stage_ids = fields.One2many('project.task.kanban.example.stage', 'example_id')

    def get_examples(self):
        data = []
        self = self.sudo()

        def append_example(example, stages):
            if stages:
                example.update({
                    'stages': stages._filter_unfold().mapped('name'),
                    'all_stages': stages.mapped('name'),
                    'folded_stages': stages._filter_fold().mapped('name')
                })
                data.append(example)

        examples = self.search_read([], ['name', 'description', 'stage_ids'])
        for example in examples:
            stages = self.stage_ids.browse(example['stage_ids'])
            append_example(example, stages)

        if self.env.company.more_project_kanban_examples:
            for project in self.env['project.project'].search([]):
                example = {
                    'name': '[P] ' + project.name,
                    'description': Markup('Example picked from already created projects'),
                    'from_database': True,
                }
                stages = project.type_ids
                append_example(example, stages)
        return data


class TaskKanbanExampleStage(models.Model):
    _name = 'project.task.kanban.example.stage'
    _description = 'Project Task Kanban Example Stage'
    _order = 'sequence'

    sequence = fields.Integer()
    example_id = fields.Many2one('project.task.kanban.example', ondelete='cascade')
    name = fields.Char(required=True)
    fold = fields.Boolean()

    def _filter_unfold(self):
        return self.filtered(lambda s: not s.fold)

    def _filter_fold(self):
        return self.filtered(lambda s: s.fold)
