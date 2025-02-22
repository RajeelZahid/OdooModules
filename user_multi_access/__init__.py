from . import models


def update_groups_post_init(env, model, groups_field, old_groups_field):
    internal_user_group = env.ref('base.group_user')
    portal_user_group = env.ref('base.group_portal')
    if model == 'ir.rule':
        for rec in env[model].search([(groups_field + '.id', '=', portal_user_group.id)]):
            setattr(rec, 'active', False)
            setattr(rec, 'force_inactive', True)

    for rec in env[model].search([(groups_field + '.id', '=', internal_user_group.id)]):
        groups = getattr(rec, groups_field)
        setattr(rec, old_groups_field, groups)
        groups = groups | portal_user_group
        setattr(rec, groups_field, groups)


def update_groups_uninstall(env, model, groups_field, old_groups_field):
    for rec in env[model].search([(old_groups_field, '!=', False)]):
        old_groups = getattr(rec, old_groups_field)
        setattr(rec, groups_field, old_groups)

    if model == 'ir.rule':
        for rec in env[model].search([('force_inactive', '=', True)]):
            setattr(rec, 'active', True)


def update_groups(env, ttype):
    func = eval('update_groups_' + ttype)
    func(env, 'ir.ui.menu', 'groups_id', 'old_groups_id')
    func(env, 'ir.ui.view', 'groups_id', 'old_groups_id')
    func(env, 'ir.actions.act_window', 'groups_id', 'old_groups_id')
    func(env, 'ir.rule', 'groups', 'old_groups')


def post_init(env):
    internal_user_group = env.ref('base.group_user')
    portal_user_group = env.ref('base.group_portal')

    access_for_portal = env['ir.model.access']
    for access in env['ir.model.access'].search([('group_id', '=', internal_user_group.id)]):
        access_for_portal |= access.copy()
    access_for_portal.write({
        'from_internal': True,
        'group_id': portal_user_group.id,
    })

    update_groups(env, 'post_init')


def uninstall_hook(env):
    IrModelAccess = env['ir.model.access']
    portal_user_group = env.ref('base.group_portal')
    IrModelAccess.search([
        ('from_internal', '=', True), ('group_id', '=', portal_user_group.id)]
    ).unlink()

    update_groups(env, 'uninstall')
