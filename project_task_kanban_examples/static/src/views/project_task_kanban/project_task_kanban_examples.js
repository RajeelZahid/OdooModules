/** @odoo-module **/

import {_t} from "@web/core/l10n/translation";
import {registry} from "@web/core/registry";
import {markup} from "@odoo/owl";
import {ORM} from "@web/core/orm_service";

const orm = new ORM
const greenBullet = markup(`<span class="o_status d-inline-block o_status_green"></span>`);
const orangeBullet = markup(`<span class="o_status d-inline-block text-warning"></span>`);
const star = markup(`<a style="color: gold;" class="fa fa-star"></a>`);
const clock = markup(`<a class="fa fa-clock-o"></a>`);

const exampleData = registry.category("kanban_examples").get('project', null);

async function getTaskKanbanExamplesData() {
    return await orm.call("project.task.kanban.example", "get_examples", [[]]);
}

async function initTaskKanbanExamples() {

    var kanban_examples = await getTaskKanbanExamplesData()
    exampleData.examples = kanban_examples.map(item => ({
        name: item.name,
        columns: item.stages,
        foldedColumns: item.folded_stages,
        get description() {
            var description = item.description + "<br><br>" +
                "Stages: " + item.stages.join(', ') + "<br>" +
                "Folded: " + item.folded_stages.join(', ')
                // + "<br><br>" +
                // "Sequence: " + item.all_stages.join(' -> ') + "<br>"
            return markup(description);
        },
        bullets: [greenBullet, orangeBullet, star, clock],
    }));

}

initTaskKanbanExamples()