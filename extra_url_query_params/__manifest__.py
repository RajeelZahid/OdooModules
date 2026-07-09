{
    'name': 'Extra URL Query Params',
    'version': '19.0.1.0.0',
    'category': 'Tools',
    'summary': 'Add extra URL query parameters.',
    'description': """
        Extend Odoo views using the add_fields URL query parameter.
    """,
    'author': 'Rajeel',
    'license': 'LGPL-3',
    'depends': ['web'],
    "website": "https://www.linkedin.com/in/rajeelzahid/",
    'assets': {
        'web.assets_backend': [
            'extra_url_query_params/static/src/**/*',
        ],
    },
    'images': ['static/description/cover.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
