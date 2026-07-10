/** @odoo-module **/

import { Component, useRef, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { _t } from "@web/core/l10n/translation";
import { standardFieldProps } from "@web/views/fields/standard_field_props";

/**
 * XML Usage:
 *
 * <field name="parts"
 *        widget="multi_selection_char"
 *        options="{
 *            'values': ['Engine', 'Rims', 'Spoilers', 'Flaps'],
 *            'separator': ',',
 *            'columns': 2,
 *            'design': 'badge',
 *            'allow_new': True
 *        }"/>
 *
 * design: 'checkbox' (default) | 'badge'
 *   checkbox — grid of checkboxes in edit; disabled checkboxes in readonly
 *   badge    — removable badge tokens + search in edit; selected badges in readonly
 *
 * allow_new: False (default) | True
 *   When True, a text input lets the user add values not in the predefined list.
 */

export class MultiSelectionCharField extends Component {
    static template = "multi_selection_char_field.MultiSelectionCharField";

    static props = {
        ...standardFieldProps,

        values: {
            type: Array,
            optional: true,
        },

        separator: {
            type: String,
            optional: true,
        },

        columns: {
            type: Number,
            optional: true,
        },

        allow_new: {
            type: Boolean,
            optional: true,
        },

        design: {
            type: String,
            optional: true,
        },
    };

    static defaultProps = {
        values: [],
        separator: ",",
        columns: 2,
        allow_new: false,
        design: "checkbox",
    };

    setup() {
        this.newValueInput = useRef("newValueInput");
        this.state = useState({ searchQuery: "" });
    }

    //--------------------------------------------------------------------------
    // Computed
    //--------------------------------------------------------------------------

    get availableValues() {
        return [...new Set(this.props.values)];
    }

    get selectedValues() {
        const value = this.props.record.data[this.props.name];

        if (!value) {
            return [];
        }

        if (!value.includes(this.props.separator)) {
            return [value.trim()];
        }

        return [...new Set(
            value
                .split(this.props.separator)
                .map((v) => v.trim())
                .filter(Boolean)
        )];
    }

    get unknownValues() {
        const available = new Set(this.availableValues);
        return this.selectedValues.filter((v) => !available.has(v));
    }

    get displayValues() {
        return [...this.availableValues, ...this.unknownValues];
    }

    /** Unselected options matching the badge search query. */
    get filteredUnselectedValues() {
        const q = this.state.searchQuery.toLowerCase().trim();
        return this.displayValues.filter(
            (v) => !this.isChecked(v) && (q === "" || v.toLowerCase().includes(q))
        );
    }

    /** True when the badge search query is a non-empty value not yet in the list. */
    get canAddNewBadge() {
        const q = this.state.searchQuery.trim();
        debugger;
        return this.props.allow_new && q !== "" && !this.displayValues.includes(q);
    }

    //--------------------------------------------------------------------------
    // Helpers
    //--------------------------------------------------------------------------

    isChecked(value) {
        return this.selectedValues.includes(value);
    }

    isUnknown(value) {
        return this.unknownValues.includes(value);
    }

    async _updateField(selected) {
        await this.props.record.update({
            [this.props.name]: [...selected].join(this.props.separator),
        });
    }

    //--------------------------------------------------------------------------
    // Checkbox design handlers
    //--------------------------------------------------------------------------

    async onChange(ev, value) {
        const selected = new Set(this.selectedValues);

        if (ev.target.checked) {
            selected.add(value);
        } else {
            selected.delete(value);
        }

        await this._updateField(selected);
    }

    async onAddNewKeydown(ev) {
        if (ev.key === "Enter") {
            ev.preventDefault();
            await this._commitNewValue(ev.target);
        }
    }

    async onAddNewClick() {
        await this._commitNewValue(this.newValueInput.el);
        this.newValueInput.el?.focus();
    }

    async _commitNewValue(input) {
        if (!input) return;
        const newValue = input.value.trim();
        if (!newValue) return;

        const selected = new Set(this.selectedValues);
        selected.add(newValue);
        input.value = "";

        await this._updateField(selected);
    }

    //--------------------------------------------------------------------------
    // Badge design handlers
    //--------------------------------------------------------------------------

    async onBadgeSelect(value) {
        const selected = new Set(this.selectedValues);
        selected.add(value);
        await this._updateField(selected);
    }

    async onRemoveBadge(value) {
        const selected = new Set(this.selectedValues);
        selected.delete(value);
        await this._updateField(selected);
    }

    async onBadgeSearchKeydown(ev) {
        if (ev.key !== "Enter") return;
        ev.preventDefault();
        if (!this.canAddNewBadge) return;

        const selected = new Set(this.selectedValues);
        selected.add(this.state.searchQuery.trim());
        this.state.searchQuery = "";

        await this._updateField(selected);
    }

    async onAddNewBadgeClick() {
        if (!this.canAddNewBadge) return;

        const selected = new Set(this.selectedValues);
        selected.add(this.state.searchQuery.trim());
        this.state.searchQuery = "";

        await this._updateField(selected);
    }
}

export const multiSelectionCharField = {
    component: MultiSelectionCharField,

    supportedTypes: ["char"],

    supportedOptions: [
        {
            label: _t("Available Values"),
            name: "values",
            type: "string",
        },
        {
            label: _t("Separator"),
            name: "separator",
            type: "string",
        },
        {
            label: _t("Columns"),
            name: "columns",
            type: "integer",
        },
        {
            label: _t("Design"),
            name: "design",
            type: "string",
        },
        {
            label: _t("Allow New Values"),
            name: "allow_new",
            type: "boolean",
        },
    ],

    extractProps: ({ options }) => ({
        values: options.values || [],
        separator: options.separator || ",",
        columns: options.columns || 2,
        design: options.design || "checkbox",
        allow_new: options.allow_new || false,
    }),
};

registry.category("fields").add("multi_selection_char", multiSelectionCharField);
