{
    'name': 'Multi Selection Char Field',
    'version': '19.0.1.0.0',
    'category': 'Tools',
    'summary': 'Multi-select widget for char fields — checkbox or badge design.',
    'description': """
        Provides the multi_selection_char widget for any Char field.
        Selected values are stored as a separator-separated string — no schema changes needed.

        Options:
          values     — list of predefined choices (e.g. ['Engine', 'Rims', 'Spoilers'])
          separator  — character used to join stored values (default: ',')
          columns    — number of grid columns for the checkbox layout (default: 2)
          design     — 'checkbox' (default) or 'badge'
          allow_new  — True/False; when True the user can type in custom values

        design = 'checkbox'
          Edit:     responsive grid of checkboxes; unknown DB values shown in warning color
          Readonly: same grid with all checkboxes disabled so context is always visible

        design = 'badge'
          Edit:     selected values shown as removable badge tokens (× to deselect);
                    search input filters unselected options; if allow_new is True the
                    search input doubles as an add-new field (Enter or + button)
          Readonly: only the selected badges are shown, no controls

        Unknown value handling:
          Values found in the database that are not in the configured list are surfaced
          automatically at the bottom in warning color and pre-selected.
    """,
    'author': 'Rajeel',
    'license': 'LGPL-3',
    'depends': ['web'],
    'assets': {
        'web.assets_backend': [
            'multi_selection_char_field/static/src/**/*',
        ],
    },
    'images': ['static/description/cover.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
