from odoo import models, fields, api


class DocumentPage(models.Model):
    _inherit = "document.page"
    _order = 'api_sequence'

    is_api_available = fields.Boolean(
        string="Is available in API",
    )
    api_sequence = fields.Integer(
        string="API Sequence"
    )
    api_highlighted_ids = fields.Many2many(
        'knowledge.page.highlight',
        relation='page_highlight_rel',
        column1='page_id',
        column2='highlight_id',
        string='Highlighted'
    )

    @api.one
    def get_api_breadcrumb(self):
        # We need to check the tree for all the parents and append them
        breadcrumb = {
            "names" : [self.name],  # String sequence
            "ids"   : [self.id],    # Int sequence
        }
        if self.parent_id:
            parent_breadcrumb = self.parent_id.get_api_breadcrumb()[0]
            breadcrumb['names'] += parent_breadcrumb.get('names')
            breadcrumb['ids'] += parent_breadcrumb.get('ids')
        return breadcrumb

    @api.one
    def _is_this_api_available(self):
        # We need to check the tree for all the parents to be api_available
        if self.parent_id:
            return bool(
                self.is_api_available and self.parent_id._is_this_api_available()[0]
            )
        else:
            return self.is_api_available

    @api.one
    def export_api_json(self, unfold=False, lang=False, breadcrumbs=False):
        if not self._is_this_api_available()[0]:
            return []
        if lang:
            record = self.with_context({'lang': lang})
        else:
            record = self.with_context({'lang': self.env.user.lang})

        if record.type == "category":
            children = record.child_ids.filtered(lambda child: child.is_api_available)
            return {
                'id'            : record.id,
                'name'          : record.name,
                'type'          : record.type,
                'content'       : record.translated_api_content,
                'api_sequence'  : record.api_sequence,
                'childs'        : list(
                    child.export_api_json(unfold, record.env.context.get('lang'))[0] for child in children
                ),
            }
        elif record.type == "content":
            to_return = {
                'name'          : record.name,
                'id'            : record.id,
                'api_sequence'  : record.api_sequence,
                'type'          : record.type,
                'tags'          : [tag.name for tag in record.tag_ids],
            }

            # if not unfold then the flow comes from categories endpoint.
            if unfold:
                to_return.update({
                    'content'    : record.translated_api_content,
                    'parent_id'  : record.parent_id.id,
                })
            else:
                to_return.update({
                    'highlighted'    : [
                        [hl.name, hl.code] for hl in record.api_highlighted_ids
                    ]
                })

            # Now for the breadcrumbs
            if breadcrumbs:
                to_return.update({
                    'breadcrumb'    : record.get_api_breadcrumb()[0]
                })
            return to_return
