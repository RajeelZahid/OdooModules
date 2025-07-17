{
    'name': 'Search many2one records with pattern',
    'version': '17.0.0.1.0',
    'category': 'Tools',
    'summary': 'Enables smarter many2one search using partial patterns by adding `{\'pattern_search\': True}` in the field context.',
    'description': """This module improves Odoo's many2one search by allowing pattern-based searching. Instead of typing full names or prefixes, users can enter partial letter sequences (e.g., "muhra" for "Muhammad Rajeel"). Just add {'pattern_search': True} in the field context to enable this smarter, faster search.""",
    'author': 'Rajeel',
    'license': 'LGPL-3',
    'depends': ['web'],
    'images': ['static/description/cover.png'],
    'data': [
    ],
    'installable': True,
    'application': False,
}
