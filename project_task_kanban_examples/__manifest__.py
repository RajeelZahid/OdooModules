# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Custom Project Task Kanban Examples',
    "version": "18.0.0.0",
    'website': 'https://www.linkedin.com/in/rajeelzahid/',
    'category': 'Services/Project',
    'sequence': 50,
    'summary': 'Create Custom Project Task Kanban Examples',
    "author": "Rajeel",
    'depends': [
        'project'
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/task_kanban_example.xml',
        'views/task_kanban_example.xml',
    ],
    'demo': [

    ],
    'installable': True,
    'application': True,
    'assets': {
        'web.assets_backend': [
            'project_task_kanban_examples/static/src/views/**/*',
            'project_task_kanban_examples/static/src/xml/**/*',
        ],
    },
    'license': 'LGPL-3',
}
