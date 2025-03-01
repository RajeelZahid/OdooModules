{
    "name": "User Multi-Access",
    "version": "18.0.0.1",
    "category": "Tools",
    "summary": """Multi Access Users""",
    "author": "Rajeel",
    "website": "https://github.com/rajeelzahid",
    "license": "OPL-1",
    "depends": [
        'base', 'web',
    ],
    "data": [
    ],
    "assets": {
        "web.assets_backend": [

        ],
        "web.assets_qweb": [

        ],
    },
    "images": ['static/description/banner.gif'],
    "installable": True,
    "application": True,

    'post_init_hook': 'post_init',
    'uninstall_hook': 'uninstall_hook',
}
