import { FormLabel } from "@web/views/form/form_label";
import { patch } from "@web/core/utils/patch";

patch(FormLabel.prototype, {
    get isDebugMode() {
        return Boolean(odoo.debug);
    },

    _onCopyClick() {
        navigator.clipboard.writeText(this.props.fieldName);
    }
})
