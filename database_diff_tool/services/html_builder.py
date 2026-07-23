"""Every bit of HTML rendered into a ``database.diff.line.remarks`` field is
built here so no comparison function ever assembles markup inline."""
from markupsafe import Markup

from odoo.tools import html_escape


def missing_target():
    return Markup('<p>Missing in target database.</p>')


def missing_subject():
    return Markup('<p>Missing in subject database.</p>')


def duplicate_key():
    return Markup(
        '<p>Duplicate comparison key detected.</p>'
        '<p>Comparison skipped.</p>'
    )


def difference_table(changes):
    """``changes`` is a dict of ``field: (subject_value, target_value)``."""
    rows = []
    for field, (subject_val, target_val) in sorted(changes.items()):
        rows.append(
            '<tr><td>%s</td><td>%s</td><td>%s</td></tr>' % (
                html_escape(str(field)),
                html_escape(str(subject_val)),
                html_escape(str(target_val)),
            )
        )
    return Markup(
        '<table class="table table-sm table-bordered">'
        '<thead><tr><th>Field</th><th>Subject</th><th>Target</th></tr></thead>'
        '<tbody>%s</tbody></table>' % ''.join(rows)
    )
