from odoo import models, fields, api, _


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
        examples = self.search_read([], ['name', 'description', 'stage_ids'])
        for example in examples:
            stages = self.stage_ids.browse(example['stage_ids'])
            example['stages'] = stages._filter_unfolded().mapped('name')
            example['all_stages'] = stages.mapped('name')
            example['folded_stages'] = stages._filter_folded().mapped('name')
            data.append(example)
        return data


class TaskKanbanExampleStage(models.Model):
    _name = 'project.task.kanban.example.stage'
    _description = 'Project Task Kanban Example Stage'
    _order = 'sequence'

    sequence = fields.Integer()
    example_id = fields.Many2one('project.task.kanban.example', ondelete='cascade')
    name = fields.Char(required=True)
    folded = fields.Boolean()

    def _filter_unfolded(self):
        return self.filtered(lambda s: not s.folded)

    def _filter_folded(self):
        return self.filtered(lambda s: s.folded)
