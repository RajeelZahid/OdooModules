/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { viewService } from "@web/views/view_service";

patch(viewService, {
    start(env, services) {
        const { loadViews: superLoadViews } = super.start(env, services);

        return {
            loadViews: async (params, options = {}) => {
                const search = new URLSearchParams(window.location.search);

                const context = {
                    ...(params.context || {}),
                };

                const addFields = search.get("add_fields");
                const highlightFields = search.get("highlight_fields");
                const orderBy = search.get("order_by");

                if (addFields) {
                    context.add_fields_view_ref = addFields;
                }

                if (highlightFields) {
                    context.highlight_fields_view_ref = highlightFields;
                }

                if (orderBy) {
                    context.order_by_view_ref = orderBy;
                }

                [
                    "decoration_info",
                    "decoration_muted",
                    "decoration_success",
                    "decoration_warning",
                    "decoration_danger",
                ].forEach((key) => {
                    const value = search.get(key);
                    debugger;
                    if (value) {
                        context[key + '_view_ref'] = value;
                    }
                });
                debugger;

                return superLoadViews(
                    {
                        ...params,
                        context,
                    },
                    options
                );
            },
        };
    },
});