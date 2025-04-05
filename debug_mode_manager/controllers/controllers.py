# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import http
from odoo.addons.portal.controllers.web import Home
from odoo.http import request
from odoo.service import security
from odoo.addons.web.controllers.utils import ensure_db


class DebugModeController(Home):

    @http.route()
    def web_client(self, s_action=None, **kw):
        ensure_db()
        if request.session.uid and security.check_session(request.session, request.env, request):
            current_user = request.env.user.browse(request.session.uid)
            if 'force_debug_mode' in kw and current_user.allow_force_debug:
                return super(DebugModeController, self).web_client(s_action, **kw)
            debug_mode = current_user.default_debug_mode
            if debug_mode and debug_mode != 'url':
                request.session.user_default_debug_mode = debug_mode

                if debug_mode == 'disallow':
                    new_mode = ''
                elif debug_mode == 'multiple':
                    new_mode = current_user.default_debug_mode_value
                else:
                    new_mode = debug_mode

                new_mode_param = new_mode and f"debug={new_mode}" or ''

                if kw.get('debug') and kw.get('debug') != new_mode:
                    new_path = request.httprequest.full_path.replace(f"debug={kw.get('debug')}", new_mode_param)
                    return request.redirect(new_path)

                elif new_mode and 'debug' not in kw:
                    new_path = request.httprequest.full_path + '&' + new_mode_param
                    return request.redirect(new_path)

        return super(DebugModeController, self).web_client(s_action, **kw)


