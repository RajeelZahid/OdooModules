/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { Dialog } from "@web/core/dialog/dialog";
import { SelectMenu } from "@web/core/select_menu/select_menu";
import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { Component, useState } from "@odoo/owl";

/**
 * Model Methods Finder Dialog Component
 * 
 * Provides interface to browse models, find methods, and open implementations
 * in external IDEs (PyCharm, VS Code).
 */
class ModelMethodsFinderDialog extends Component {
    static template = "model_methods_finder.dialog";
    static components = { Dialog, SelectMenu };
    static props = {
        all_models: { type: Object },
        close: { type: Function },
    };

    setup() {
        this.state = useState({
            model_name: null,
            method_name: null,
            selected_model_methods: [],
            all_inheritances: [],
            all_implementations: [],
        });
    }

    /**
     * Handle model selection from dropdown
     * @param {string} value - Selected model name
     */
    async setSelectModelName(value) {
        this.state.model_name = value;
        this.state.selected_model_methods = [];
        this.state.method_name = null;
        this.state.all_inheritances = [];
        this.state.all_implementations = [];
        
        if (value) {
            await this.findMethods();
        }
    }

    /**
     * Handle method selection from dropdown
     * @param {string} value - Selected method name
     */
    setSelectMethodName(value) {
        this.state.method_name = value;
        this.state.all_implementations = [];
    }

    /**
     * Fetch all methods for selected model
     */
    async findMethods() {
        try {
            this.state.selected_model_methods = await rpc('/web/dataset/call_kw', {
                model: this.state.model_name,
                method: 'get_all_methods',
                args: [],
                kwargs: {},
            });
        } catch (error) {
            console.error('Error fetching methods:', error);
            // add comment - Add user notification for error
        }
    }

    /**
     * Clear all inheritances
     */
    async clearInheritances() {
        this.state.all_inheritances = []
    }

    /**
     * Fetch all inheritance files for selected model
     */
    async findInheritances() {
        try {
            this.state.all_inheritances = await rpc('/web/dataset/call_kw', {
                model: this.state.model_name,
                method: 'get_all_inheritance',
                args: [],
                kwargs: {},
            });
        } catch (error) {
            console.error('Error fetching inheritances:', error);
            // add comment - Add user notification for error
        }
    }

    /**
     * Fetch all implementations for selected method
     */
    async findImplementations() {
        if (!this.state.method_name) {
            return;
        }
        
        try {
            this.state.all_implementations = await rpc('/web/dataset/call_kw', {
                model: this.state.model_name,
                method: 'get_all_method_impls',
                args: [[], this.state.method_name],
                kwargs: {},
            });
        } catch (error) {
            console.error('Error fetching implementations:', error);
            // add comment - Add user notification for error
        }
    }

    /**
     * Open file in PyCharm at specified line
     * @param {Array} impl - [filepath, line_number]
     */
    async _onOpenInPycharm(impl) {
        try {
            await rpc('/web/dataset/call_kw', {
                model: 'base',
                method: 'open_in_pycharm',
                args: [[], impl[0], impl[1]],
                kwargs: {},
            });
        } catch (error) {
            console.error('Error opening in PyCharm:', error);
            // add comment - Add user notification for error
        }
    }

    /**
     * Open file in VS Code at specified line
     * @param {Array} impl - [filepath, line_number]
     */
    async _onOpenInVscode(impl) {
        try {
            await rpc('/web/dataset/call_kw', {
                model: 'base',
                method: 'open_in_vscode',
                args: [[], impl[0], impl[1]],
                kwargs: {},
            });
        } catch (error) {
            console.error('Error opening in VS Code:', error);
            // add comment - Add user notification for error
        }
    }
}

/**
 * Debug menu item for Model Methods Finder
 * @param {Object} params - Component and environment
 * @returns {Object} Debug menu item configuration
 */
export function modelMethodsFinder({ component, env }) {
    return {
        type: "item",
        description: _t("Model Methods Finder"),
        callback: async () => {
            try {
                const all_models = await rpc('/web/dataset/call_kw', {
                    model: 'base',
                    method: 'get_all_installed_models',
                    args: [],
                    kwargs: {},
                });
                env.services.dialog.add(ModelMethodsFinderDialog, { all_models });
            } catch (error) {
                // todo Add user notification for error
                console.error('Error loading models:', error);
            }
        },
        sequence: 270,
        section: "ui",
    };
}

// Register the debug menu item
registry
    .category("debug")
    .category("default")
    .add("modelMethodsFinder", modelMethodsFinder);
