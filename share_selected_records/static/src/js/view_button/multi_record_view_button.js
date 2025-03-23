/** @odoo-module **/

import {MultiRecordViewButton} from '@web/views/view_button/multi_record_view_button';
import {patch} from "@web/core/utils/patch";
import {useService} from "@web/core/utils/hooks";
import {ORM} from "@web/core/orm_service";


const orm = new ORM
function fallbackCopyTextToClipboard(text) {
    var textArea = document.createElement("textarea");
    textArea.value = text;

    // Avoid scrolling to bottom
    textArea.style.top = "0";
    textArea.style.left = "0";
    textArea.style.position = "fixed";

    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();

    try {
        var successful = document.execCommand('copy');
        var msg = successful ? 'successful' : 'unsuccessful';
        console.log('Fallback: Copying text command was ' + msg);
    } catch (err) {
        console.error('Fallback: Oops, unable to copy', err);
    }

    document.body.removeChild(textArea);
}

patch(MultiRecordViewButton.prototype, {
    setup() {
        this.notification = useService("notification");
        super.setup(...arguments);
    },

    async onClick() {
        const {clickParams, list} = this.props;
        if (clickParams.name === 'copy_shareable_link') {
            const resIds = await list.getResIds(true);
            var paths = window.location.pathname.split('/')
            clickParams.buttonContext = {
                active_domain: this.props.domain,
                active_ids: resIds,
                active_model: list.resModel,
                active_action: paths[paths.length - 1]
            };
            var link = await orm.call("base", "generate_link", [clickParams.buttonContext])
            try {
                await navigator.clipboard.writeText(link);
                this.notification.add('Link Copied!', {type: 'success', stick: false})
            } catch (err) {
                fallbackCopyTextToClipboard(link);
                this.notification.add('Failed to copy link!', {type: 'error', stick: false})
            }
        }
        await super.onClick(...arguments);
    }
});