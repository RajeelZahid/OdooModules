import { Record } from "@web/model/relational_model/record";
import { patch } from "@web/core/utils/patch";

function safeEval(expression, context = {}) {
    return Function(...Object.keys(context), `"use strict";\n${expression}`)
           (...Object.values(context));
}

// Patch the Record class to add serverless onchange functionality
patch(Record.prototype, {
    _getServerlessOnchangeValues(changes) {
        const new_values = {...this._values, ...this._changes};
        const old_values = this._values;
        const modelConfig = this.model.config
        let results = {};

        for (const [fieldName, fieldValue] of Object.entries(changes)) {
            const fieldConfig = modelConfig.fields[fieldName];
            if (!fieldConfig || !fieldConfig.serverless_onchange) continue;

            for (const [targetField, formula] of Object.entries(fieldConfig.serverless_onchange)) {
                let computedValue;
                try {
                    computedValue = safeEval(formula, {self: fieldValue, new_values, old_values}); // sandboxing needed if user-defined
                } catch (e) {
                    console.warn(`Error evaluating formula for ${targetField}:`, e);
                    continue;
                }

                // Validate result based on target field type
                const targetConfig = modelConfig.fields[targetField];
                if (!targetConfig) continue;

                switch (targetConfig.type) {
                    case "text":
                    case "char":
                    case "selection":
                    case "html":
                        computedValue = String(computedValue ?? "");
                        break;
                    case "integer":
                    case "float":
                    case "monetary":
                        if (isNaN(Number(computedValue))) {
                            console.warn(`Invalid number for field ${targetField}`);
                            continue;
                        }
                        computedValue = Number(computedValue);
                        break;
                    case "boolean":
                        computedValue = Boolean(computedValue);
                        break;
                    default:
                        console.warn(`Unsupported field type ${targetConfig.type} for ${targetField}`);
                        continue;
                }

                results[targetField] = computedValue;
            }
        }

        return results;
    },

    async _update(changes, { withoutOnchange, withoutParentUpdate } = {}) {
        var res = await super._update(changes, {withoutOnchange, withoutParentUpdate})
        let onchangeServerlessValues = this._getServerlessOnchangeValues(changes);
        this._applyChanges(changes, onchangeServerlessValues);
        return res
    }
});

