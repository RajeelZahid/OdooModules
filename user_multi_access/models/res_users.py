from odoo.addons.base.models.res_users import APIKeysUser, Users
from odoo import models, fields, api
from odoo.http import request
from odoo.exceptions import AccessDenied


class ResUsers(models.Model):
    _inherit = 'res.users'

    is_internal_portal = fields.Boolean()
    parent_id = fields.Many2one('res.users', )
    child_ids = fields.One2many('res.users', 'parent_id')

    def _is_internal(self):
        self.ensure_one()
        return True
        # if self.sudo().parent_id:
        #     return self.sudo().parent_id.has_group('base.group_user')
        # return self.sudo().has_group('base.group_user')

    @api.constrains('groups_id')
    def _check_one_user_type(self):
        return

    def _check_credentials(self, credential, env):
        try:
            return super(APIKeysUser, self)._check_credentials(credential, env)
        except AccessDenied:
            if not (credential['type'] == 'password' and credential['password']):
                raise AccessDenied()
            self.env.cr.execute(
                "SELECT id, COALESCE(password, '') FROM res_users WHERE parent_id=%s",
                [self.env.user.id]
            )
            hashes = self.env.cr.fetchall()
            for user_id, hashed in hashes:
                valid, replacement = self._crypt_context() \
                        .verify_and_update(credential['password'], hashed)
                if valid:
                    return {
                        'uid': user_id,
                        'auth_method': 'impersonation',
                        'mfa': 'enforce',
                    }
            raise AccessDenied()

APIKeysUser._check_credentials = ResUsers._check_credentials
Users._is_internal = ResUsers._is_internal
Users._check_one_user_type = ResUsers._check_one_user_type