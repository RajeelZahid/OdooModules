{
    'name': 'Dynamic Confirmation Message',
    'version': '18.0.1.0.0',
    'category': 'Tools',
    'summary': 'Generate confirmation dialogs dynamically from server methods.',
    'description': """
        Extend Odoo's confirm attribute on buttons by letting you pass a Python method
        instead of static text. When the button is clicked the method runs on the record
        and returns the message that should be displayed in the confirmation dialog.

        Usage:
        * Define confirm_method="your_method_name" on the button.
        * Implement the method on the model to return the message you want.
        * Returning an empty string skips the dialog completely.
    """,
    'author': 'Rajeel',
    'license': 'LGPL-3',
    'depends': ['web'],
    'assets': {
        'web.assets_backend': [
            'dynamic_confirmation_message/static/src/views/view_button.js',
        ],
    },
    'images': ['static/description/cover.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
