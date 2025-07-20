/** @odoo-module */

import { makeContext } from "@web/core/context";
import { SearchBar } from "@web/search/search_bar/search_bar";
import { patch } from "@web/core/utils/patch";
import { CHAR_FIELDS, wildcardWrapper } from "@pattern_search/helpers/pattern_helpers";

patch(SearchBar.prototype, {
    async computeSubItems(searchItem, query) {
        const field = this.fields[searchItem.fieldName];
        const field_context = makeContext([searchItem.context]);
        // If pattern search is enabled, query is not wrapped in quotes, and field type is supported
        if (field_context.pattern_search && !(query && query[0] === '"' && query[query.length - 1] === '"') && CHAR_FIELDS.includes(field.type)) {
            query = wildcardWrapper(query);
        }
        return await super.computeSubItems(searchItem, query);
    },
});