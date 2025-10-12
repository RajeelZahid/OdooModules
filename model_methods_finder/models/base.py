# -*- coding: utf-8 -*-
# Copyright 2024 Rajeel
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import functools
import inspect
import os
from odoo import api, models

# Skip these directories when searching for methods
SKIP_DIRS = ['_cache']


def _search_lineno_for_class(filepath, class_name):
    """Find line number where class is defined in file."""
    lineno = 1
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f.readlines(), 1):
                if line.strip().startswith(f'class {class_name}'):
                    lineno = i
                    break
    except (OSError, IOError):
        # File might not exist or be readable
        pass
    return lineno


class Base(models.AbstractModel):
    """Extend base model with methods finder functionality."""

    _inherit = 'base'

    @api.model
    def get_all_inheritance(self):
        """
        Get all inheritance files for current model.
        
        Returns:
            list: List of [filepath, line_number] tuples
        """
        inheritances = []
        for cls in self._model_classes:
            if cls != object and cls._name == self._name:
                filepath = inspect.getsourcefile(cls)
                if filepath:
                    lineno = _search_lineno_for_class(filepath, cls.__name__)
                    if [filepath, lineno] not in inheritances:
                        inheritances.append([filepath, lineno])
        return inheritances

    @api.model
    def get_all_methods(self):
        """
        Get all callable methods for current model instance.
        
        Returns:
            list: List of dicts with 'value' and 'label' keys
        """
        methods = []
        for attr_name in dir(self):
            if attr_name in SKIP_DIRS:
                continue
            attr = getattr(self, attr_name)
            if callable(attr):
                methods.append(attr_name)
        return [{'value': m, 'label': m} for m in methods]

    def get_all_method_impls(self, method_name):
        """
        Get all method implementations for given method name.
        
        Args:
            method_name (str): Name of the method to find
            
        Returns:
            list: List of [filepath, line_number] tuples
        """
        model_name = self._name
        if not method_name or not model_name:
            return []
        if model_name not in self.env:
            return []
        
        implementations = []
        cls = type(self.env[model_name])
        
        # Walk the Method Resolution Order (MRO)
        for base in inspect.getmro(cls):
            if method_name in base.__dict__:
                method = base.__dict__[method_name]
                try:
                    # Handle decorated methods
                    if hasattr(method, '__wrapped__'):
                        method = method.__wrapped__
                    
                    # Handle partial methods
                    if isinstance(method, functools.partial):
                        method_name = str(method.func).split(' ')[1]
                        method = method.func
                    
                    filepath = inspect.getsourcefile(method)
                    if filepath:
                        if isinstance(method, type):
                            lineno = _search_lineno_for_class(filepath, method.__name__)
                        else:
                            lineno = inspect.getsourcelines(method)[1]
                        implementations.append([filepath, lineno])
                except Exception:
                    # Some method types are not supported
                    error_msg = ("Unable to find this method. "
                               "Might be sanitization not supported yet for this type of method.")
                    implementations.append([error_msg, 0])
        return implementations

    def open_in_pycharm(self, file_path, line_number):
        """Open file in PyCharm at specified line number."""
        # todo: Add error handling and validation
        os.system(f'pycharm --line {line_number} "{file_path}"')

    def open_in_vscode(self, file_path, line_number):
        """Open file in VS Code at specified line number."""
        # todo: Add error handling and validation
        os.system(f'code --goto "{file_path}":{line_number}')

    @api.model
    def get_all_installed_models(self):
        """
        Get all installed models in the system.
        
        Returns:
            list: List of dicts with 'value' and 'label' keys
        """
        all_models = sorted(list(self.env))[1:]  # Skip '_unknown' model
        return [{'value': m, 'label': m} for m in all_models]
