/** @odoo-module */

export const CHAR_FIELDS = ["char", "html", "many2many", "many2one", "one2many", "text", "properties"];

export function wildcardWrapper(string){
    string = string ? string : '';
    return `%${string.split('').join('%')}%`;
}