"""Uniform read-only access to a "Subject" or "Target" Odoo database.

Two flavours of :class:`Source` are provided:

* :class:`LocalSource` reuses the current, in-process Odoo environment
  (fast native ORM access, no credentials needed).
* :class:`RemoteSource` reaches another Odoo database over XML-RPC using
  url/db/username/password.

Both expose the same ``search_read(model, domain, fields)`` method so the
comparison engine never needs to know which kind of source it is talking to.
"""
import xmlrpc.client

from odoo.exceptions import ValidationError
from odoo.tools.translate import _


def model_based_context(model):
    context = {'active_test': False}
    if model == 'ir.ui.menu':
        context['ir.ui.menu.full_list'] = True
    return context


class Source:
    db_name = False

    def search_read(self, model, domain, fields):
        raise NotImplementedError


class LocalSource(Source):
    """Reuses the current Odoo environment (same process, same cursor)."""

    def __init__(self, env, db_name):
        self.env = env
        self.db_name = db_name
        self.url = env['res.config.settings'].get_base_url()

    def search_read(self, model, domain, fields):
        return self.with_context(model_based_context(model)).env[model].sudo().search_read(domain or [], fields)


class RemoteSource(Source):
    """Connects to another Odoo database through XML-RPC."""

    def __init__(self, url, db_name, username, password):
        self.url = url
        self.db_name = db_name
        self.username = username
        self.password = password

        try:
            common = xmlrpc.client.ServerProxy('%s/xmlrpc/2/common' % url)
            uid = common.authenticate(db_name, username, password, {})
        except Exception as exc:
            raise ValidationError(
                _('Could not connect to %(url)s (database "%(db)s"): %(error)s')
                % {'url': url, 'db': db_name, 'error': exc}
            ) from exc

        if not uid:
            raise ValidationError(
                _('Invalid credentials for database "%s".') % db_name
            )

        self.uid = uid
        self.models = xmlrpc.client.ServerProxy('%s/xmlrpc/2/object' % url)

    def search_read(self, model, domain, fields):
        try:
            return self.models.execute_kw(
                self.db_name, self.uid, self.password,
                model, 'search_read',
                [domain or []],
                {'fields': list(fields), 'context': model_based_context(model)},
            )
        except Exception as exc:
            raise ValidationError(
                _('Failed to read "%(model)s" from database "%(db)s": %(error)s')
                % {'model': model, 'db': self.db_name, 'error': exc}
            ) from exc


def get_source(env, *, use_current_env, url, db_name, username, password):
    """Build the right :class:`Source` from wizard-style inputs."""
    if use_current_env:
        return LocalSource(env, env.cr.dbname)

    if not (url and username and password):
        raise ValidationError(
            _('DB name, URL, username and password are all required to connect to "%s".') % resolved_db
        )

    return RemoteSource(url, db_name, username, password)
