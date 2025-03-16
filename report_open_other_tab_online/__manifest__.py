# -*- coding: utf-8 -*-
{
    'name': 'Open Report with Other Tab (Odoo Online)',
    "version": "18.0.0.1.0",
    "category": "Tools",
    'summary': """Open PDF/HTML reports in new tabs""",
    'description': """This module enhances the Odoo reporting experience by enabling developers to open reports in a new tab for PDF or HTML. This functionality allows developers to directly preview changes made to reports simply by refreshing the report's tab. switch between PDF and HTML formats directly through the URL, eliminating the need for additional steps and saving valuable development time.
    """,
    'author': 'Rajeel',
    'images': ['static/description/cover.gif'],
    'depends': ['web'],
    'data': [
        'views/ir_actions_report.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
    'assets': {
        'web.assets_backend': [
            'report_open_other_tab/static/src/js/report_utils.js',
        ]
    }
}
