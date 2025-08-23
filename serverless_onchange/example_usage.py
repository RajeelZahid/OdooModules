# Example usage of serverless_onchange functionality
# This file demonstrates how to define fields with serverless_onchange parameter

from odoo import fields, models

class ExampleModel(models.Model):
    _name = 'example.model'
    _description = 'Example Model for Serverless Onchange'

    # Example field that triggers serverless onchange
    boolean_field = fields.Boolean(serverless_onchange={
        'selection_field': """
if (self){
    return 'option2';
} else {
    return 'option3';
}
"""
    })
    additional = """'<br/><br/>Integer Field current value: ' + String(new_values.integer_field ?? 0) +
        '<br/>Integer Field saved value: ' + String(old_values.integer_field ?? 0) +
        '<br/><br/>Float Field current value: ' + String(new_values.float_field ?? 0.0) + 
        '<br/>Float Field saved value: ' + String(old_values.float_field ?? 0.0) """
    integer_field = fields.Integer(serverless_onchange={
        'note': "return 'Changed from Integer Field' +" + additional
    })

    float_field = fields.Float(serverless_onchange={
        'char_field': "return 'Float Field value: ' + String(self)",
        'note': "return 'Changed from Float Field' + " + additional
    })
    char_field = fields.Char()
    selection_field = fields.Selection([
        ('option1', 'Option 1'),
        ('option2', 'Boolean Field True'),
        ('option3', 'Boolean Field False')
    ], serverless_onchange={
        'boolean_field': """
if (self === 'option2'){
    return true
} else if (self === 'option3'){
    return false
} return new_values.boolean_field
"""
    })
    html_field = fields.Html()
