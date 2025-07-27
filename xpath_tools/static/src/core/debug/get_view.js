/** @odoo-module */

import { registry } from "@web/core/registry";
import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { _t } from "@web/core/l10n/translation";
import { parseXML, findXPath, getMatchingXMLs } from '@xpath_tools/helpers/xml_helpers';


const debugRegistry = registry.category("debug");

export const placeholder = {
    input_xml: 'Select from above or paste tag like <field name=\'name\'/>',
    output_xpath: 'One or more XPaths found will appear here...',
    input_xpath: 'Enter XPath like //field[@name=\'name\']',
    output_xml: 'Matching sub-XMLs or errors will appear here',
}

export class GetViewDialog extends Component {
    static template = "web.DebugMenu.GetViewDialog";
    static components = {Dialog};
    static props = {
        arch: {type: String},
        close: {type: Function},
        placeholder: {type: Object}
    };

    setup() {
        this.state = useState({});
    }

    _onCopyClickXPath(xpath) {
        navigator.clipboard.writeText(xpath);
    }

    setInputXml(value) {
        this.state.input_xml = value;
        let xpaths = findXPath(this.props.arch, value);
        if (typeof xpaths == 'string') {
            this.state.output_xpath_error = xpaths
            this.state.output_xpath = null
        } else {
            this.state.output_xpath_error = null
            this.state.output_xpath = xpaths
        }
    }

    pointerUpArch() {
        var selection = window.getSelection().toString().trim();
        if (selection.length > 0) {
            const xml_arch = this.props.arch;
            if (xml_arch.includes(selection)) {
                if (parseXML(selection)){
                    this.setInputXml(selection)
                    return;
                }
                selection = selection.replace(/(<\w+[^>]*)(?<!\/)>$/, '$1/>');
                if (parseXML(selection)){
                    this.setInputXml(selection)
                }
            }
        }
    }

    setInputXpath(value) {
        this.state.input_xpath = value
        let xmls = getMatchingXMLs(this.props.arch, value)
        if (typeof xmls == 'string') {
            this.state.output_xml_error = xmls
            this.state.output_xml = null
        } else {
            this.state.output_xml_error = null
            this.state.output_xml = xmls
        }
    }

}

export function getView({component, env}) {
    return {
        type: "item",
        description: _t("Computed Arch"),
        callback: () => {
            env.services.dialog.add(GetViewDialog, {arch: component.env.config.rawArch, placeholder});
        },
        sequence: 270,
        section: "ui",
    };
}

debugRegistry.category("view").remove("getView");
debugRegistry.category("view").add("getView", getView);