from odoo.tools.translate import translate_sql_constraint
from odoo.tools.misc import DotDict
from psycopg2 import errors
from odoo.exceptions import ValidationError
import odoo.service.model
# from odoo.service.model import _as_validation_error as _as_validation_error_base
from odoo.http import request
import json


def def_sql_constraint(cr, key):
    cr.execute(f"""SELECT definition FROM ir_model_constraint WHERE name='{key}' and type='u'""")
    return cr.fetchone()[0]


def _as_validation_error(env, exc):
    """ Return the IntegrityError encapsuled in a nice ValidationError """

    unknown = env._('Unknown')
    model = DotDict({'_name': 'unknown', '_description': unknown})
    field = DotDict({'name': 'unknown', 'string': unknown})
    for _name, rclass in env.registry.items():
        if exc.diag.table_name == rclass._table:
            model = rclass
            field = model._fields.get(exc.diag.column_name) or field
            break

    match exc:
        case errors.NotNullViolation():
            return ValidationError(env._(
                "The operation cannot be completed:\n"
                "- Create/update: a mandatory field is not set.\n"
                "- Delete: another model requires the record being deleted."
                " If possible, archive it instead.\n\n"
                "Model: %(model_name)s (%(model_tech_name)s)\n"
                "Field: %(field_name)s (%(field_tech_name)s)\n",
                model_name=model._description,
                model_tech_name=model._name,
                field_name=field.string,
                field_tech_name=field.name,
            ))

        case errors.ForeignKeyViolation():
            return ValidationError(env._(
                "The operation cannot be completed: another model requires "
                "the record being deleted. If possible, archive it instead.\n\n"
                "Model: %(model_name)s (%(model_tech_name)s)\n"
                "Constraint: %(constraint)s\n",
                model_name=model._description,
                model_tech_name=model._name,
                constraint=exc.diag.constraint_name,
            ))

    if exc.diag.constraint_name in env.registry._sql_constraints:
        err_msg = env._("The operation cannot be completed: %s",
                        translate_sql_constraint(env.cr, exc.diag.constraint_name, env.context.get('lang', 'en_US')), )

        if hasattr(exc, 'show_detail'):
            if hasattr(exc, 'rec_name'):
                additional_details = f" - Record: {exc.rec_name}"
            else:
                additional_details = f" - Table: {exc.diag.table_name}"
            additional_details += f"\n - Constrain name: {exc.diag.constraint_name}"
            if exc.diag.message_primary:
                additional_details += f"\n - Error msg: {exc.diag.message_primary}"
                if exc.diag.message_detail:
                    additional_details += f"\n              {exc.diag.message_detail}"
            if cons_definition := def_sql_constraint(env.cr, exc.diag.constraint_name):
                additional_details += f"\n - Definition: {cons_definition}"
            if hasattr(request, 'params'):
                'kwargs' in request.params and 'specification' in request.params['kwargs'] and request.params['kwargs'].pop('specification')
                additional_details += f"\n - Params sent to server: {json.dumps(request.params, indent=4, default=str)}"
            if hasattr(exc, 'vals') and hasattr(exc, 'cause_method'):
                additional_details += f"\n - Modified data to {exc.cause_method} {exc.rec_name}: {json.dumps(exc.vals, indent=4, default=str)}"

            err_msg += env._("\n\nMore details below (If you do not know what to do, copy the details and share with your friendly support service) :\n"
                             "Disable the 'show detailed constrain errors' from general settings > debugging tools to turn off more details.\n%s",
                             additional_details)
        else:
            err_msg += "\n\nIf you are really stuck here, enable the 'show detailed constrain errors' from general settings > debugging tools."

        return ValidationError(err_msg)

    return ValidationError(env._("The operation cannot be completed: %s", exc.args[0]))


odoo.service.model._as_validation_error = _as_validation_error