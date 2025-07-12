{
    'name': 'Field Technical Name in List/Form Views',
    'version': '18.0.0.1.0',
    'category': 'Tools',
    'summary': 'Display and copy field technical names next to field labels',
    'description': """This module displays the technical field name directly next to the field label in form and list views.
Each field comes with a dedicated copy button in form view.""",
    'author': 'Rajeel',
    'license': 'LGPL-3',
    'depends': ['web'],
    'images': ['static/description/cover.gif'],
    'data': [
    ],
    'assets': {
        'web.assets_backend': [
            'field_technical_name/static/src/views/**/*',
        ]
    },
    'installable': True,
    'application': False,
}
