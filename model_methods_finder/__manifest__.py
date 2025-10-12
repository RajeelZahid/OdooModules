{
    'name': 'Model Methods Finder',
    'version': '18.0.1.0.0',
    'category': 'Tools',
    'summary': 'Find and explore model methods with IDE integration.',
    'description': """
        Developer tool to search method implementations across models and open them in IDE.
        
        Features:
        * Browse all installed models
        * List all methods for a selected model
        * Find method implementations across inheritance chain
        * Open implementations directly in PyCharm or VS Code
        * Quick access via Debug menu
    """,
    'author': 'Rajeel',
    'license': 'LGPL-3',
    'depends': ['web'],
    'images': ['static/description/cover.png'],
    'data': [],
    'assets': {
        'web.assets_backend': [
            'model_methods_finder/static/src/**/*',
        ]
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}
