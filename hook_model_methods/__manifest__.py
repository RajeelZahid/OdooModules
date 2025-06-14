{
    'name': 'Hook Model Methods',
    'version': '18.0.0.1.1',
    'category': 'Tools',
    'summary': 'Custom hook system for Odoo models that eliminates super() calls by injecting pre/post logic cleanly and modularly.',
    'description': """This module introduces a custom hook system for Odoo models, allowing developers to cleanly inject pre/post logic into existing methods, including normal methods, onchange, compute, and more, without overriding via super().
By using @install_hooks, developers can attach logic directly to model functions, making code more modular, maintainable, and less prone to errors caused by traditional super() chains.""",
    'author': 'Rajeel',
    'images': ['static/description/cover.png'],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
