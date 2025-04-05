from odoo import fields, models, api
from odoo.exceptions import UserError
from odoo.addons.web.models.ir_http import ALLOWED_DEBUG_MODES

ALLOWED_DEBUG_MODES_KEYS = list(ALLOWED_DEBUG_MODES)
ALLOWED_DEBUG_MODES_KEYS[0] = 'url'
ALLOWED_DEBUG_MODES_KEYS += ['multiple', 'disallow']
ALLOWED_DEBUG_MODES_VALS = ['Always Get from URL', '1 (Always Debug)', 'assets (Always Debug with Assets)', 'tests (Always Debug with Tests)', 'disable-t-cache (Always Debug with t-cache Disabled)', 'Debug with Mutliple Modes', 'Always Disallow']

DEBUG_MODES_SELECTION = list(zip(ALLOWED_DEBUG_MODES_KEYS, ALLOWED_DEBUG_MODES_VALS))

field1_help = """Set default debug mode to use system-wide
Get From URL: Always get from URL
1: Always Debug
assets: Debug with Assets
tests: Debug with Tests
Multiple: Debug with multiple modes e.g. assets and tests together
Disallow Always: Disallow user to not use the debug mode in any way"""
field3_help = "Allow forcing the debug to any mode for user by passing the force_debug_mode= param in URL"


class ResUsers(models.Model):
    _inherit = 'res.users'

    default_debug_mode = fields.Selection(DEBUG_MODES_SELECTION, default='url', help=field1_help)
    default_debug_mode_value = fields.Char('Multiple Debug Mode Values')
    allow_force_debug = fields.Boolean(help=field3_help)

    @api.constrains('default_debug_mode_value')
    def check_debug_mode_value(self):
        if self.default_debug_mode_value:
            for mode in self.default_debug_mode_value.split(','):
                if mode not in ALLOWED_DEBUG_MODES:
                    raise UserError(f"{mode} is not a valid debug mode!\nValid values are {', '.join(ALLOWED_DEBUG_MODES[1:])}.")

