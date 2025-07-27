{
    'name': 'XPath Tools for View Architecture',
    'version': '18.0.0.1.0',
    'category': 'Tools',
    'summary': 'Helps developers convert XML tags to XPath and explore views using XPath expressions.',
    'description': """This module enhances the Computed Arch / Get View experience in Odoo 18, making it easier for junior developers to work with XML views.

Features:
- Convert any complete XML tag with attributes into an accurate XPath expression.
- Input XPath expressions and extract all related sub-XML snippets from the view architecture.

Designed to simplify and accelerate view customization and debugging using a clean, developer-friendly interface.""",
    'author': 'Rajeel',
    'license': 'LGPL-3',
    'depends': ['web'],
    'images': ['static/description/cover.png'],
    'data': [
        'views/ir_ui_view.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'xpath_tools/static/src/**/*',
        ]
    },
    'installable': True,
    'application': False,
}
