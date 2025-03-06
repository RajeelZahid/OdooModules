/** @odoo-module **/

import { KanbanColumnQuickCreate } from "@web/views/kanban/kanban_column_quick_create";
import { KanbanColumnExamplesDialog } from "@web/views/kanban/kanban_column_examples_dialog";
import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";


patch(KanbanColumnQuickCreate.prototype, {
    showExamples() {
        this.dialog.add(KanbanColumnExamplesDialog, {
            examples: this.props.exampleData.examples,
            applyExamplesText:
                this.props.exampleData.applyExamplesText || _t("Use This For My Kanban"),
            applyExamples: (index) => {
                const { examples, foldField} = this.props.exampleData;
                const {columns, foldedColumns = [], allColumns = columns.concat(foldedColumns)} = examples[index];
                for (const groupName of allColumns) {
                    if (columns.includes(groupName)) {
                        this.props.onValidate(groupName);
                    } else if (foldedColumns.includes(groupName)) {
                        this.props.onValidate(groupName, foldField);
                    }
                }
            },
        });
    }

})
