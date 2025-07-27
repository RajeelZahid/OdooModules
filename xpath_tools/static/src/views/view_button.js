/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { ViewButton } from "@web/views/view_button/view_button";
import { useService } from "@web/core/utils/hooks";
import { placeholder, GetViewDialog } from "@xpath_tools/core/debug/get_view";

patch(ViewButton.prototype, {
    setup() {
        super.setup()
        this.orm = useService('orm')
    },

    async onClick(ev) {
        if (['xpath-tools-computed-view', 'xpath-tools-one-view'].includes(this.props.id)) {
            var arch;
            if (this.props.id === 'xpath-tools-one-view') {
                arch = this.props.record.data.arch_base;
            }
            else {  // button id == xpath-tools-computed-view
                const view_id = this.props.record.resId;
                arch = await this.orm.call('ir.ui.view', 'read_template', [view_id]);
            }
            this.env.services.dialog.add(GetViewDialog, {arch, placeholder});
            return
        }
        return super.onClick(ev);
    }
});