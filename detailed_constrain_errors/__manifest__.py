{
    "name": "Detailed Constrain Errors",
    "version": "18.0.0.1.0",
    "category": "Tools",
    "summary": """Provides detailed information when constraint errors occur.""",
    "description": """This module enhances the standard Odoo error handling mechanism by providing detailed information when a constraint error is triggered. It helps developers and users quickly identify and resolve issues related to constraint violations by offering valuable debugging information such as the name of the record that caused the error, the specific constraint that was violated, the constraint's definition, the parameters sent to the server, and the data that led to the error. The module is compatible with Community, Enterprise, and Odoo.sh editions.""",
    "author": "Rajeel",
    "website": "https://www.linkedin.com/in/rajeelzahid/",
    'images': ['static/description/cover.png'],
    "license": "OPL-1",
    "depends": [
        'base', 'base_setup'
    ],
    "data": [
        'views/res_config_settings.xml',
    ],
    "installable": True,
    "application": False,
}
