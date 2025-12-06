/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { ViewButton } from "@web/views/view_button/view_button";

patch(ViewButton.prototype, {

    async onClick(ev) {
        if (this.props.attrs && this.props.attrs.confirm_method && this.props.attrs.confirm_method !== '') {
            const res_id = this.props.record.resId;
            const res_model = this.env.model.config.resModel;
            try {
                const confirm_message = await this.env.model.orm.call(res_model, this.props.attrs.confirm_method, [res_id]);
                if (typeof confirm_message === "string"){
                    if (confirm_message === '') {
                        if (this.props.clickParams.confirm) {
                            delete this.props.clickParams.confirm
                        }
                    } else {
                        this.props.clickParams.confirm = confirm_message + `\n\nClick Ok to continue ${this.props.string}.`
                    }
                }
            } catch (error) {
                this.env.services.notification.add(`Method "${this.clickParams.confirm}" encountered an error or was not found in model "${res_model}"`, {type: 'danger'});
                return false;
            }
        }
        return super.onClick(ev);
    }
});
