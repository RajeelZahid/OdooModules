"""Comparison rules for modules, models, fields, menus and views.

Every function takes a subject :class:`~.connection.Source` and a target
:class:`~.connection.Source`, loads each side into a ``dict[key] -> record``
in a single pass (O(n)), and returns a list of ``database.diff.line``-ready
dicts (``type``, ``record_name``, ``remarks``, ``severity``).
"""
from . import html_builder as hb

MODULE_FIELDS = ['name', 'state']
MODEL_FIELDS = ['model']
FIELD_FIELDS = [
    'model', 'name', 'relation', 'ttype', 'copied', 'related', 'readonly',
    'required', 'index', 'company_dependent', 'relation_table', 'column1', 'column2',
]
FIELD_COMPARE_ATTRS = [f for f in FIELD_FIELDS if f not in ('model', 'name')]
MENU_FIELDS = ['name', 'parent_path', 'active', 'sequence']
VIEW_FIELDS = ['key', 'name', 'active', 'arch_db']


def _index(records, key_func):
    """Group records by key, tracking any duplicate keys separately."""
    index = {}
    duplicate_keys = set()
    for rec in records:
        key = key_func(rec)
        if key in index:
            duplicate_keys.add(key)
        else:
            index[key] = rec
    return index, duplicate_keys


def _build_lines(diff_type, subject_index, subject_dupes, target_index, target_dupes, compare_fields):
    lines = []
    seen = set()

    for key in sorted(subject_dupes | target_dupes):
        seen.add(key)
        remarks = hb.duplicate_key()
        lines.append({
            'type': diff_type,
            'record_name': key,
            'remarks': remarks,
            'remarks_plain_text': remarks.striptags(),
            'severity': 'warning',
        })

    subject_keys = set(subject_index) - seen
    target_keys = set(target_index) - seen

    for key in sorted(subject_keys - target_keys):
        remarks = hb.missing_target()
        lines.append({
            'type': diff_type,
            'record_name': key,
            'subject_db_record_id': subject_index[key]['id'],
            'remarks': remarks,
            'remarks_plain_text': remarks.striptags(),
            'severity': 'critical',
        })

    for key in sorted(target_keys - subject_keys):
        remarks = hb.missing_subject()
        lines.append({
            'type': diff_type,
            'record_name': key,
            'target_db_record_id': target_index[key]['id'],
            'remarks': remarks,
            'remarks_plain_text': remarks.striptags(),
            'severity': 'critical',
        })

    for key in sorted(subject_keys & target_keys):
        subject_rec = subject_index[key]
        target_rec = target_index[key]
        changes = {}
        for field in compare_fields:
            subject_val = subject_rec.get(field)
            target_val = target_rec.get(field)
            if subject_val != target_val:
                changes[field] = (subject_val, target_val)
        if changes:
            remarks = hb.difference_table(changes)
            lines.append({
                'type': diff_type,
                'record_name': key,
                'subject_db_record_id': subject_index[key]['id'],
                'target_db_record_id': target_index[key]['id'],
                'remarks': remarks,
                'remarks_plain_text': remarks.striptags(),
                'severity': 'warning',
            })

    return lines


def compare_modules(subject_source, target_source):
    subject_records = subject_source.search_read('ir.module.module', [], MODULE_FIELDS)
    target_records = target_source.search_read('ir.module.module', [], MODULE_FIELDS)
    subject_index, subject_dupes = _index(subject_records, lambda r: r['name'])
    target_index, target_dupes = _index(target_records, lambda r: r['name'])
    return _build_lines('module', subject_index, subject_dupes, target_index, target_dupes, ['state'])


def compare_models(subject_source, target_source):
    subject_records = subject_source.search_read('ir.model', [], MODEL_FIELDS)
    target_records = target_source.search_read('ir.model', [], MODEL_FIELDS)
    subject_index, subject_dupes = _index(subject_records, lambda r: r['model'])
    target_index, target_dupes = _index(target_records, lambda r: r['model'])
    # Only "availability" was specified for models, and it is treated as a
    # no-op (redundant with missing-in-subject/target), so there is no
    # field-level diff here - only existence is compared.
    return _build_lines('model', subject_index, subject_dupes, target_index, target_dupes, [])


def compare_fields(subject_source, target_source):
    subject_records = subject_source.search_read('ir.model.fields', [], FIELD_FIELDS)
    target_records = target_source.search_read('ir.model.fields', [], FIELD_FIELDS)
    key_func = lambda r: '%s.%s' % (r['model'], r['name'])
    subject_index, subject_dupes = _index(subject_records, key_func)
    target_index, target_dupes = _index(target_records, key_func)
    return _build_lines('field', subject_index, subject_dupes, target_index, target_dupes, FIELD_COMPARE_ATTRS)


def _load_menu_paths(source):
    """Return menu records keyed by their name-based path, e.g.
    ``Settings/Users & Companies/Users/Users`` instead of ``1/3/61/61``."""
    records = source.search_read('ir.ui.menu', [], MENU_FIELDS)
    name_by_id = {rec['id']: rec['name'] for rec in records}
    result = []
    for rec in records:
        raw_path = (rec.get('parent_path') or '').strip('/')
        ids = [int(part) for part in raw_path.split('/') if part]
        names = [name_by_id.get(i, str(i)) for i in ids] if ids else [rec['name']]
        result.append({
            'id': rec['id'],
            'key': '/'.join(names),
            'active': rec['active'],
            'sequence': rec['sequence'],
        })
    return result


def compare_menus(subject_source, target_source):
    subject_records = _load_menu_paths(subject_source)
    target_records = _load_menu_paths(target_source)
    subject_index, subject_dupes = _index(subject_records, lambda r: r['key'])
    target_index, target_dupes = _index(target_records, lambda r: r['key'])
    return _build_lines('menu', subject_index, subject_dupes, target_index, target_dupes, ['active', 'sequence'])


def compare_views(subject_source, target_source):
    subject_records = subject_source.search_read('ir.ui.view', [], VIEW_FIELDS)
    target_records = target_source.search_read('ir.ui.view', [], VIEW_FIELDS)
    key_func = lambda r: ('key:%s' % r['key']) if r.get('key') else ('name:%s' % r['name'])
    subject_index, subject_dupes = _index(subject_records, key_func)
    target_index, target_dupes = _index(target_records, key_func)

    lines = []
    seen = set()
    for key in sorted(subject_dupes | target_dupes):
        seen.add(key)
        remarks = hb.duplicate_key()
        lines.append({
            'type': 'view',
            'record_name': key,
            'remarks': remarks,
            'remarks_plain_text': remarks.striptags(),
            'severity': 'warning',
        })

    subject_keys = set(subject_index) - seen
    target_keys = set(target_index) - seen

    for key in sorted(subject_keys - target_keys):
        remarks = hb.missing_target()
        lines.append({
            'type': 'view',
            'record_name': key,
            'subject_db_record_id': subject_index[key]['id'],
            'remarks': remarks,
            'remarks_plain_text': remarks.striptags(),
            'severity': 'critical',
        })

    for key in sorted(target_keys - subject_keys):
        remarks = hb.missing_subject()
        lines.append({
            'type': 'view',
            'record_name': key,
            'target_db_record_id': target_index[key]['id'],
            'remarks': remarks,
            'remarks_plain_text': remarks.striptags(),
            'severity': 'critical',
        })

    for key in sorted(subject_keys & target_keys):
        subject_rec = subject_index[key]
        target_rec = target_index[key]
        changes = {}
        for field in ('name', 'active'):
            if subject_rec.get(field) != target_rec.get(field):
                changes[field] = (subject_rec.get(field), target_rec.get(field))
        # arch_db is compared but its content is never displayed - only the
        # fact that it differs is shown, per plan.txt.
        if subject_rec.get('arch_db') != target_rec.get('arch_db'):
            changes['arch_db'] = ('Diff', 'Diff')
        if changes:
            remarks = hb.difference_table(changes)
            lines.append({
                'type': 'view',
                'record_name': key,
                'subject_db_record_id': subject_index[key]['id'],
                'target_db_record_id': target_index[key]['id'],
                'remarks': remarks,
                'remarks_plain_text': remarks.striptags(),
                'severity': 'warning',
            })

    return lines
