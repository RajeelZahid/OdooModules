{
    'name': 'Database Diff Tool',
    'version': '18.0.1.0.0',
    'category': 'Tools',
    'summary': 'Compare modules, models, fields, menus and views between two Odoo databases.',
    'description': """
Database Diff Tool
===================
Developer utility that compares two Odoo databases - the current one, or two
databases reached through XML-RPC - and generates a read-only report of
differences in:

  * Installed modules
  * Models
  * Fields
  * Menus
  * Views

The report is stored in Odoo so it can be reviewed and shared later.
    """,
    'author': 'Rajeel',
    'license': 'LGPL-3',
    'depends': ['base', 'web'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/database_diff_create_views.xml',
        'views/database_diff_views.xml',
        'views/database_diff_line_views.xml',
        'views/database_diff_menus.xml',
    ],
    'images': ['static/description/cover.gif'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
