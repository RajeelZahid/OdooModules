{
    'name': 'Serverless Onchange',
    'version': '18.0.0.1.0',
    'category': 'Technical',
    'summary': 'Serverless onchange functionality for Odoo',
    'description': """
        This module provides serverless onchange functionality that allows
        field value changes to be computed client-side without server calls.
        
        Features:
        - Client-side field value computation
        - Support for various field types
        - Formula-based field dependencies
    """,
    'author': 'Rajeel',
    'license': 'LGPL-3',
    'depends': [
        'base', 'web'
    ],
    'images': ['static/description/cover.png'],
    'data': [
    ],
    'assets': {
        'web.assets_backend': [
            'serverless_onchange/static/src/model/relation_model/record.js',
        ],
    },
    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': False,
}
