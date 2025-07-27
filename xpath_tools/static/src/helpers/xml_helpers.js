/** @odoo-module */

// Parses XML string into XML Document
export function parseXML(xmlStr) {
    try {
        const parser = new DOMParser();
        const xmlDoc = parser.parseFromString(xmlStr, "application/xml");

        const errorNode = xmlDoc.querySelector("parsererror");
        if (errorNode) throw new Error("Invalid XML syntax");

        return xmlDoc;
    } catch (e) {
        return null;
    }
}

// Builds XPath for a node within the provided XML document
function getNodeXPath(node, xmlDoc) {
    if (!node || node.nodeType !== 1) return "";
    if (!node.parentNode || node === xmlDoc.documentElement)
        return "/" + buildNodeSelector(node);

    return getNodeXPath(node.parentNode, xmlDoc) + "/" + buildNodeSelector(node);
}

// Builds a selector for the current node using its attributes or index
function buildNodeSelector(node) {
    const attrs = ["name", "id", "t-name", "t-field", "class"];
    for (let attr of attrs) {
        const val = node.getAttribute(attr);
        if (val) return `${node.nodeName}[@${attr}='${val}']`;
    }

    const siblings = Array.from(node.parentNode.children)
        .filter(n => n.nodeName === node.nodeName);
    const index = siblings.indexOf(node) + 1;
    return siblings.length > 1 ? `${node.nodeName}[${index}]` : node.nodeName;
}

// Compares two nodes shallowly (node name and attributes only)
function nodesEqualShallow(a, b) {
    if (a.nodeName !== b.nodeName) return false;

    const aAttrs = a.attributes;
    const bAttrs = b.attributes;
    if (aAttrs.length !== bAttrs.length) return false;

    for (let i = 0; i < aAttrs.length; i++) {
        const name = aAttrs[i].name;
        if (a.getAttribute(name) !== b.getAttribute(name)) return false;
    }
    return true;
}

// Finds XPath(s) for the given HTML tag string inside the XML string
export function findXPath(xmlStr, tagHTML) {
    const xmlDoc = parseXML(xmlStr);
    if (!xmlDoc) return "Invalid or missing XML.";

    tagHTML = tagHTML.trim();
    if (!tagHTML) return "";

    try {
        const dummy = new DOMParser().parseFromString(`<root>${tagHTML}</root>`, "application/xml");
        const searchNode = dummy.documentElement.firstElementChild;
        if (!searchNode) return "Invalid tag input.";

        const candidates = xmlDoc.getElementsByTagName(searchNode.nodeName);
        const matches = [];

        for (let node of candidates) {
            if (nodesEqualShallow(node, searchNode)) {
                matches.push(getNodeXPath(node, xmlDoc));
            }
        }

        // return matches.length && matches
        return matches.length ? matches : "Tag not found in XML.";
        return matches.length ? matches.join("\n") : "Tag not found in XML.";
    } catch (e) {
        return "Tag parse error.";
    }
}

// Gets XML nodes that match the given XPath in the given XML string
export function getMatchingXMLs(xmlStr, xpath) {
    const xmlDoc = parseXML(xmlStr);
    if (!xmlDoc) return "Invalid or missing XML.";

    xpath = xpath.trim();
    if (!xpath) return "";

    try {
        const result = xmlDoc.evaluate(xpath, xmlDoc, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);
        const matches = [];

        for (let i = 0; i < result.snapshotLength; i++) {
            const node = result.snapshotItem(i);
            const xml = new XMLSerializer().serializeToString(node);
            matches.push(xml);
        }

        return matches.length ? matches : "No matching nodes.";
    } catch (e) {
        return "XPath error: " + e.message;
    }
}

