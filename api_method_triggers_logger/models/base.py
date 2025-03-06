from odoo import models
import logging
import functools
import inspect
import types
from odoo.addons.base.models.ir_model import MODULE_UNINSTALL_FLAG

_logger = logging.getLogger(__name__)
LOG_APIS = ['onchange', 'constrains', 'depends', 'unlink']
ALLOWED_MODELS = []  # Empty means All
DISALLOWED_MODELS = []  # Empty means None


def _get_func_name(func):
    if isinstance(func, functools.partial):
        return str(func).split('.')[1].split()[0]
    return func.__name__


def _log_func_source(func):
    file_path, line_number = inspect.getsourcefile(func), inspect.getsourcelines(func)[1]
    _logger.info(fr'File "{file_path}", line {line_number}')


def _handle_partial_func(method, method_name):
    if isinstance(method, functools.partial):
        method_name = str(method.func).split(' ')[1]
        method = method.func
    return method, method_name


class Model(models.AbstractModel):
    _inherit = 'base'

    def log_method_source(self, method=False, method_name=False):
        if not method and not method_name:
            _logger.error("No method or method name provided")
            return
        if method_name:
            method = getattr(self, method_name, False)
            if not callable(method):
                _logger.error(f"{self._name}.{method_name}() not found")
                return
        if method:
            method_name = _get_func_name(method)
        method, method_name = _handle_partial_func(method, method_name)
        _logger.info(f"'{method_name}' of '{self._name}'. Source below.")
        _log_func_source(method)

    def _log_api_method_call(self, api_type, method, field_name):
        if api_type not in LOG_APIS:
            return
        if (ALLOWED_MODELS and self._name not in ALLOWED_MODELS) or (DISALLOWED_MODELS and self._name in DISALLOWED_MODELS):
            return
        try:
            method_name = _get_func_name(method)
            if api_type == 'constrains':
                if method_name == '_constraint_methods':
                    return
            if isinstance(field_name, list):  # cause can be from any of the fields
                if len(field_name) == 1:
                    field_name = field_name[0]
                else:
                    field_name = '(' + ', '.join(field_name) + ')'
            method, method_name = _handle_partial_func(method, method_name)  # partial function can be because of change_default attr of field
            _logger.info(f"'{method_name}' was executed because of {api_type} api linked to '{self._name}.{field_name}'. Source below.")
            _log_func_source(method)
        except Exception as E:
            ...

    def _log_onchange_api(self, field_name):
        for method in self._onchange_methods.get(field_name, ()):
            self._log_api_method_call('onchange', method, field_name)

    def _apply_onchange_methods(self, field_name, result):
        """ "ONCHANGE" Logs will be done after all methods executed """
        super(Model, self)._apply_onchange_methods(field_name, result)
        try:
            self._log_onchange_api(field_name)
        except Exception as E:
            ...

    def _log_constrain_api(self, field_names, excluded_names):
        field_names = set(field_names)
        excluded_names = set(excluded_names)
        for check in self._constraint_methods:
            if (not field_names.isdisjoint(check._constrains)
                    and excluded_names.isdisjoint(check._constrains)):
                self._log_api_method_call('constrains', check, list(field_names.intersection(check._constrains)))

    def _validate_fields(self, field_names, excluded_names=()):
        """ "CONSTRAINS" Logs will be done after all methods executed """
        field_names = list(field_names)
        excluded_names = list(excluded_names)
        super(Model, self)._validate_fields(field_names, excluded_names)
        try:
            self._log_constrain_api(field_names, excluded_names)
        except Exception as E:
            ...

    def _log_depends_api(self, field):
        if field.store:
            if callable(field.compute):
                if field.compute.__name__ == '_compute_related':  # do not log for store & related field
                    return
                method = field.compute
            else:
                method = getattr(self, field.compute)
            if hasattr(method, '_depends'):
                field_names = method._depends
                if isinstance(field_names, types.LambdaType):  # lambda can also be provided as api.depends param
                    field_names = method._depends(self)
                self._log_api_method_call('depends', method, list(field_names))

    def _compute_field_value(self, field):
        """ "DEPENDS/COMPUTE" Logs will be done after method executed """
        super(Model, self)._compute_field_value(field)
        try:
            self._log_depends_api(field)
        except Exception as E:
            ...

    def _log_unlink_api(self):
        for func in self._ondelete_methods:
            if func._ondelete or not self._context.get(MODULE_UNINSTALL_FLAG):
                self._log_api_method_call('unlink', func, '')

    def unlink(self):
        """ "UNLINK" Logs will be done after method executed """
        res = super(Model, self).unlink()
        try:
            self._log_unlink_api()
        except Exception as E:
            ...
        return res
