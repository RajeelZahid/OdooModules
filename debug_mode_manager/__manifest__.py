# -*- coding: utf-8 -*-
{
    'name': 'Debug Mode Manager',
    "version": "18.0.0.1.0",
    "category": "Tools",
    'summary': """Manage debugging preferences and permissions with advanced options and URL-based force debug control.""",
    'description': """This module provides extended capabilities for debugging management in Odoo. By introducing two new fields in the Users form view and it enables administrators to assign specific debug preferences and empower users with the ability to override debugging via URL parameters.
The field offers seven tailored debug options, providing granular control over user behavior. With the addition of users can force specific debug modes through the URL parameter, giving unparalleled flexibility during development or troubleshooting.
""",
    'author': 'Rajeel',
    'images': ['static/description/cover.gif'],
    'depends': ['web'],
    'data': [
        'views/res_users.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
