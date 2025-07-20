/** @odoo-module */

import { makeContext } from "@web/core/context";
import { SearchModel } from "@web/search/search_model";
import { patch } from "@web/core/utils/patch";
import { CHAR_FIELDS, wildcardWrapper } from "@pattern_search/helpers/pattern_helpers";

patch(SearchModel.prototype, {
    addAutoCompletionValues(searchItemId, autocompleteValue) {
        const searchItem = this.searchItems[searchItemId];
        const field = this.searchViewFields[searchItem.fieldName];
        const field_context = makeContext([searchItem.context]);
        // If pattern search is enabled in context and field type is one of the supported text-like fields
        if (field_context.pattern_search && typeof autocompleteValue.value == 'string' && CHAR_FIELDS.includes(field.type)) {
            autocompleteValue.value = wildcardWrapper(autocompleteValue.value);
        }
        super.addAutoCompletionValues(searchItemId, autocompleteValue);
    },
});
