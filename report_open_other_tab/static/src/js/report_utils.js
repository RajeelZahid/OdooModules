/** @odoo-module **/
import { registry } from "@web/core/registry";

function _openReportUrl(action, type, env) {
    let url = `/report/${type}/${action.report_name}`;

    const contextDict = Object.assign(
        {},
        action.context || {},
        env && env.services && env.services.user ? env.services.user.context : {}
    );

    if (action.data && JSON.stringify(action.data) !== "{}") {
        const options = encodeURIComponent(JSON.stringify(action.data));
        const context = encodeURIComponent(JSON.stringify(contextDict));
        url += `?options=${options}&context=${context}`;
    } else {
        if (contextDict.active_ids) {
            url += `/${contextDict.active_ids.join(",")}`;
        }
        const context = encodeURIComponent(JSON.stringify(contextDict));
        url += `?context=${context}`;
    }
    window.open(url);
}

async function _openPrintWindowTab(action, options, env, type) {
    _openReportUrl(action, type, env);
    return Promise.resolve(true);
}

registry.category("ir.actions.report handlers").add("open_with_another_tab_handler", async (action, options, env) => {
    if (["qweb-pdf", "qweb-html"].includes(action.report_type) && action.open_with_another_tab) {
        let report_type = action.report_type.split('-')[1];
        return _openPrintWindowTab(action, options, env, report_type);
    } else {
        return Promise.resolve(false);
    }
});
