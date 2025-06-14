from odoo import models
# from odoo.tools import install_hooks  # will be deprecated in future versions
from odoo.models import install_hooks


@install_hooks
class ResPartner(models.Model):
    _inherit = 'res.partner'

    def _pre_hook_name_create(self, name):
        # do something before calling name_create
        ...

    def _post_hook_name_create(self, name):
        # do something after calling name_create
        ...
