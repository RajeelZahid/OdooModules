from odoo.addons.base.models.assetsbundle import JavascriptAsset, transpile_javascript
import re


def handle_date_js(content):
    re_smartDateRegex_f = r"const smartDateRegex[\s\S]*?\);"
    re_smartDateRegex_r = r"""const smartDateAllUnitsRegex = RegExp( "([+-]\\\\s*\\\\d+\\\\s*(?:"+Object.keys(smartDateUnits).join('|')+"))", "gi" );
    const smartDateRegex = RegExp( "^\\\\s*([+-])\\\\s*(\\\\d+)\\\\s*("+Object.keys(smartDateUnits).join('|')+")\\\\s*$", "i" );"""

    re_smartDateUnits_f = r"const smartDateUnits[\s\S]*?\};"
    re_smartDateUnits_r = r"""const smartDateUnits = {
    days: "days",
    months: "months",
    weeks: "weeks",
    years: "years",
    yrs: "years",
    yr: "years",
    hours: "hours",
    hrs: "hours",
    hr: "hours",
    minutes: "minutes",
    min: "minutes",
    d: "days",
    m: "months",
    w: "weeks",
    y: "years",
    h: "hours",
    x: "minutes",
};
"""

    re_parseSmartDateInput_f = r"function parseSmartDateInput[\s\S]*?(?=/\*\*)"
    re_parseSmartDateInput_r = r"""function parseSmartDateUnit(value, date) { // +1m , luxonDate
    const match = value.match(smartDateRegex); // [+, 1, m, +1m] 
    if (match) {
        const offset = parseInt(match[2], 10);
        const unit = smartDateUnits[(match[3] || "d").toLowerCase()];
        if (match[1] === "+") {
            date = date.plus({ [unit]: offset });
        } else {
            date = date.minus({ [unit]: offset });
        }
        return date;
    }
    return false;
}

function extractDateTime(value) {
    let splitted = value.split(',');
    let date = DateTime.fromFormat(splitted[0], localization.dateTimeFormat);
    let smartInput = splitted[0];
    if (! date.c) {
        date = DateTime.fromFormat(splitted[0], localization.dateFormat);
        if (! date.c) {
            date = DateTime.local();
        }
        else {
            smartInput = splitted[1];
        }
    } else {
        smartInput = splitted[1];
    }
    return [date, smartInput];
}

function parseSmartDateInput(value) {  // +1m +1d
    if (['today', 'td', 'current', 'crnt', 'now', '0'].includes(value)) {
        value = '+0d';
    } else if (['tomorrow', 'tmrw', 'tmr', 'next day', 'nextday', 'nxtday'].includes(value)) {
        value = '+1d';
    } else if (['yesterday', 'ystr', 'yester', 'previous day', 'prev day', 'prevday'].includes(value)) {
        value = '-1d';
    }
    let [date, smartInput] = extractDateTime(value);
    const matches = smartInput.match(smartDateAllUnitsRegex);  // [+1m,+1d]
    if (matches) {
        matches.forEach((match) => { // +1m
            date = parseSmartDateUnit(match, date);
        })
        return date;
    }
    return false;
}
"""
    for find_re, replace_re in {
        re_smartDateUnits_f: re_smartDateUnits_r,
        re_smartDateRegex_f: re_smartDateRegex_r,
        re_parseSmartDateInput_f: re_parseSmartDateInput_r
    }.items():
        content = re.sub(find_re, replace_re, content)

    return content


class JavascriptAssetChild(JavascriptAsset):

    @property
    def content(self):
        content = super(JavascriptAsset, self).content
        if self.url == '/web/static/src/core/l10n/dates.js':
            content = handle_date_js(content)
        if self.is_transpiled:
            if not self._converted_content:
                self._converted_content = transpile_javascript(self.url, content)
            return self._converted_content
        return content


JavascriptAsset.content = JavascriptAssetChild.content
