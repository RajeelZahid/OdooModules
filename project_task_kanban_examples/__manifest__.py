# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Custom Project Task Kanban Examples',
    "version": "18.0.0.1.0",
    'website': 'https://www.linkedin.com/in/rajeelzahid/',
    'category': 'Services/Project',
    'sequence': 50,
    'summary': 'Create and use custom project task kanban examples',
    'description': """It is designed to enhance project management in Odoo by providing users with the ability to create and utilize custom Kanban boards. 
This module allows users to design their own Kanban examples tailored to their specific project needs and seamlessly integrate them with existing Kanban boards from other projects.""",
    "author": "Rajeel",
    'depends': [
        'project'
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/task_kanban_example.xml',
        'views/task_kanban_example.xml',
        'views/res_config_settings.xml',
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
    'images': ['static/description/cover.gif'],
}
