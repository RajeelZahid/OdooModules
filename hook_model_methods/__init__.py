from odoo import tools, models
import inspect
from functools import wraps

import logging

_logger = logging.getLogger(__name__)


def install_hooks(cls):
    """
    Automatically installs all _pre_hook_<method> and _post_hook_<method> hooks,
    passing only the arguments that the hook function accepts.
    """
    method_hooks = {}

    for attr in dir(cls):
        if attr.startswith('_pre_hook_'):
            target_method_name = attr[len('_pre_hook_'):]
            method_hooks.setdefault(target_method_name, {})['pre'] = attr
        elif attr.startswith('_post_hook_'):
            target_method_name = attr[len('_post_hook_'):]
            method_hooks.setdefault(target_method_name, {})['post'] = attr

    for method_name, hooks in method_hooks.items():
        original_method = getattr(cls, method_name, None)

        if not original_method or getattr(original_method, '_is_hooked', False):
            continue

        def make_wrapper(orig_method, pre_hook_name=None, post_hook_name=None):
            @wraps(orig_method)
            def wrapper(self, *args, **kwargs):
                bound_args = {'self': self, **_build_call_args(orig_method, self, *args, **kwargs)}

                if pre_hook_name:
                    pre_hook = getattr(self, pre_hook_name, None)
                    if pre_hook:
                        _call_with_filtered_args(pre_hook, bound_args)

                result = orig_method(self, *args, **kwargs)

                if post_hook_name:
                    post_hook = getattr(self, post_hook_name, None)
                    if post_hook:
                        _call_with_filtered_args(post_hook, bound_args)

                return result
            wrapper._is_hooked = True
            return wrapper

        wrapped = make_wrapper(
            original_method,
            hooks.get('pre'),
            hooks.get('post')
        )
        setattr(cls, method_name, wrapped)

    return cls


def _build_call_args(method, self, *args, **kwargs):
    """
    Uses inspect to bind the actual call arguments to parameter names.
    """
    try:
        sig = inspect.signature(method)
        bound = sig.bind(self, *args, **kwargs)
        bound.apply_defaults()
        return dict(bound.arguments)
    except Exception:
        return {}  # Fallback if binding fails


def _call_with_filtered_args(func, all_args):
    """
    Filters args to only pass what's accepted by the hook.
    """
    try:
        sig = inspect.signature(func)
        accepted_params = sig.parameters.keys()
        filtered_args = {
            k: v for k, v in all_args.items() if k in accepted_params
        }
        func(**filtered_args)
    except Exception as e:
        _logger.warning(f"Hook call failed: {func.__name__}: {e}")


setattr(tools, 'install_hooks', install_hooks)
setattr(models, 'install_hooks', install_hooks)


class HookInstallerMixin(models.AbstractModel):
    _inherit = 'base'

    def _register_hook(self):
        """
        Override base model building logic to inject hooks into ALL models during registry setup.
        """
        res = super()._register_hook()
        install_hooks(type(self))
        return res
