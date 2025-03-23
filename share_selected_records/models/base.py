from odoo import models, api
from lxml import etree


class Model(models.AbstractModel):
    _inherit = 'base'

    def copy_shareable_link(self):
        return None

    @api.model
    def generate_link(self, kwargs):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        res_ids = kwargs.get('active_ids')
        res_ids = str(res_ids)[1: -1].replace(' ', '')
        link_id = self.env['shared.recs.link.wizard'].create({
            'res_ids': res_ids,
            'res_model': kwargs.get('active_model'),
            'action': kwargs.get('active_action')
        }).id
        return f"{base_url}/odoo/shared-link/{link_id}"

    @api.model
    def get_view(self, view_id=None, view_type='form', **options):
        result = super(Model, self).get_view(view_id, view_type, **options)
        if view_type != 'list':
            return result
        node = etree.fromstring(result['arch'])
        copy_link_btn_node = etree.Element(
            "button", attrib={
                'name': 'copy_shareable_link',
                'type': 'object',
                'string': 'Copy Shareable Link'
            })

        if not (header_node := node.xpath('//header')):
            header_node = [etree.Element('header')]
            node.insert(0, header_node[0])

        header_node[0].insert(0, copy_link_btn_node)
        result['arch'] = etree.tostring(node, encoding="unicode").replace('\t', '')
        return result