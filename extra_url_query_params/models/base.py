import logging

from lxml import etree

from odoo import api, models

_logger = logging.getLogger(__name__)


class Base(models.AbstractModel):
    _inherit = "base"

    DECORATION_KEYS = [
        "decoration_info",
        "decoration_muted",
        "decoration_success",
        "decoration_warning",
        "decoration_danger",
    ]

    # ---------------------------------------------------------
    # Context helpers
    # ---------------------------------------------------------

    @api.model
    def _get_context_fields(self, key):
        raw = self.env.context.get(key)
        if not raw or not isinstance(raw, str):
            return []
        return [x.strip() for x in raw.split(",") if x.strip()]

    @api.model
    def _get_add_fields(self):
        return self._get_context_fields("add_fields_view_ref")

    @api.model
    def _get_highlight_fields(self):
        return self._get_context_fields("highlight_fields_view_ref")

    @api.model
    def _get_order_by(self):
        value = self.env.context.get("order_by_view_ref")
        return value if isinstance(value, str) else False

    @api.model
    def _get_decorations(self):
        result = {}
        for key in self.DECORATION_KEYS:
            value = self.env.context.get(key + '_view_ref')
            if value:
                result[key.replace("_", "-")] = value
        return result

    # ---------------------------------------------------------
    # XML helpers
    # ---------------------------------------------------------

    @api.model
    def _get_arch_container(self, node, view_type):
        if view_type == "list":
            containers = node.xpath("//list | //tree")
        elif view_type == "form":
            containers = node.xpath("//sheet")
        else:
            return None
        return containers[0] if containers else node

    # ---------------------------------------------------------
    # Add fields
    # ---------------------------------------------------------

    @api.model
    def _apply_add_fields_to_arch(self, arch, view_type, field_names):
        if not field_names:
            return arch

        node = etree.fromstring(arch)
        container = self._get_arch_container(node, view_type)

        if container is None:
            return arch

        fields_to_add = []

        for field_name in field_names:
            if field_name not in self._fields:
                _logger.warning(
                    'Unknown field "%s" on model "%s"',
                    field_name,
                    self._name,
                )
                continue

            fields_to_add.append(field_name)

        if not fields_to_add:
            return arch

        parent = container
        index = len(parent)

        if view_type == "form":
            group = etree.Element("group")
            for field_name in fields_to_add:
                group.append(
                    etree.Element(
                        "field",
                        {
                            "name": field_name,
                            "readonly": "1",
                        },
                    )
                )
            parent.append(group)

        elif view_type == "list":
            for field_name in fields_to_add:
                existed = node.xpath(f'//field[@name="{field_name}"]')
                if existed:
                    existed = existed[0]
                    if (
                        existed.attrib.get("column_invisible")
                        or existed.attrib.get("optional") == "hide"
                    ):
                        existed.getparent().remove(existed)

                parent.insert(
                    index,
                    etree.Element(
                        "field",
                        {
                            "name": field_name,
                            "readonly": "1",
                            "optional": "show",
                        },
                    ),
                )
                index += 1

        return etree.tostring(node, encoding="unicode")

    # ---------------------------------------------------------
    # Highlight fields
    # ---------------------------------------------------------

    @api.model
    def _apply_highlight_fields_to_arch(self, arch, field_names):
        if not field_names:
            return arch

        node = etree.fromstring(arch)

        for field_name in field_names:
            if field_name not in self._fields:
                continue

            for field_node in node.xpath(f'//field[@name="{field_name}"]'):
                classes = field_node.get("class", "").split()
                if "bg-info-light" not in classes:
                    classes.append("bg-info-light")
                field_node.set("class", " ".join(classes))

        return etree.tostring(node, encoding="unicode")

    # ---------------------------------------------------------
    # default_order
    # ---------------------------------------------------------

    @api.model
    def _apply_default_order(self, arch, view_type, order_by):
        if not order_by:
            return arch

        node = etree.fromstring(arch)

        if view_type == "list":
            roots = node.xpath("//list | //tree")
        elif view_type == "kanban":
            roots = node.xpath("//kanban")
        else:
            return arch

        if roots:
            roots[0].set("default_order", order_by)

        return etree.tostring(node, encoding="unicode")

    # ---------------------------------------------------------
    # Decorations
    # ---------------------------------------------------------

    @api.model
    def _apply_decorations(self, arch, view_type, decorations):
        if view_type != "list":
            return arch

        if not decorations:
            return arch

        node = etree.fromstring(arch)

        roots = node.xpath("//list | //tree")
        if not roots:
            return arch

        root = roots[0]

        for attr, expr in decorations.items():
            root.set(attr, expr)

        return etree.tostring(node, encoding="unicode")

    # ---------------------------------------------------------
    # get_view
    # ---------------------------------------------------------

    @api.model
    def get_view(self, view_id=None, view_type="form", **options):
        result = super().get_view(view_id=view_id, view_type=view_type, **options)

        if view_type in ("list", "form"):

            add_fields = self._get_add_fields()
            if add_fields:
                result["arch"] = self._apply_add_fields_to_arch(
                    result["arch"],
                    view_type,
                    add_fields,
                )

            highlight_fields = self._get_highlight_fields()
            if highlight_fields:
                result["arch"] = self._apply_highlight_fields_to_arch(
                    result["arch"],
                    highlight_fields,
                )

        if view_type in ("list", "kanban"):
            order_by = self._get_order_by()
            if order_by:
                result["arch"] = self._apply_default_order(
                    result["arch"],
                    view_type,
                    order_by,
                )

        if view_type in ("list",):
            decorations = self._get_decorations()
            if decorations:
                result["arch"] = self._apply_decorations(
                    result["arch"],
                    view_type,
                    decorations,
                )

        return result