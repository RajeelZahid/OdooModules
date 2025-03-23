# -*- coding: utf-8 -*-
{
    'name': 'Share Selected Records',
    "version": "18.0.0.1.0",
    "category": "Tools",
    'summary': """Copy sharable links for records with a single click. """,
    'description': """This Odoo module revolutionizes how users interact with records by enabling seamless sharing. Users can effortlessly select multiple records and generate a unique, shareable link with a single click. This link is automatically copied to the clipboard for immediate use. Designed to streamline collaboration and enhance accessibility, the module is perfect for businesses looking to share record data efficiently within teams or with external stakeholders. The intuitive button feature ensures minimal learning curve while maximizing productivity.""",
    'author': 'Rajeel',
    'images': ['static/description/cover.gif'],
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'wizards/shared_recs_link_wizard_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
    'assets': {
        'web.assets_backend': [
            'share_selected_records/static/src/js/view_button/multi_record_view_button.js',
        ]
    }
}
