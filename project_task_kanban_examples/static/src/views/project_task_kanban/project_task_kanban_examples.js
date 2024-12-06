/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { renderToMarkup } from '@web/core/utils/render';
import { markup } from "@odoo/owl";

const greenBullet = markup(`<span class="o_status d-inline-block o_status_green"></span>`);
const orangeBullet = markup(`<span class="o_status d-inline-block text-warning"></span>`);
const star = markup(`<a style="color: gold;" class="fa fa-star"></a>`);
const clock = markup(`<a class="fa fa-clock-o"></a>`);

const exampleData = registry
            .category("kanban_examples")
            .get('project', null);

exampleData.examples.push(
    {
        name: _t('Custom #1'),
        columns: [_t('New'), _t('Analyzing'), _t('In Progress'), _t('Done')],
        foldedColumns: [_t('Cancelled')],
        get description() {
            return renderToMarkup("project.example.custom1");
        },
        bullets: [greenBullet, orangeBullet, star, clock],
    },{
        name: _t('Custom #2'),
        columns: [_t('New'), _t('Checking'), _t('Testing'), _t('Done')],
        foldedColumns: [_t('Rejected')],
        get description() {
            return renderToMarkup("project.example.custom1");
        },
        bullets: [greenBullet, orangeBullet, star, clock],
    },
)

registry.category("kanban_examples").remove('project');
registry.category("kanban_examples").add('project', exampleData);
