/** @odoo-module */

import { Many2XAutocomplete } from "@web/views/fields/relational_utils";
import { patch } from "@web/core/utils/patch";
import { wildcardWrapper } from "@pattern_search/helpers/pattern_helpers";

patch(Many2XAutocomplete.prototype, {
    search(name) {
        return this.orm.call(this.props.resModel, "name_search", [], {
            name: wildcardWrapper(name),
            operator: "ilike",
            args: this.props.getDomain(),
            limit: this.props.searchLimit + 1,
            context: this.props.context,
        });
    }
});
