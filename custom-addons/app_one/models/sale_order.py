from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = "sale.order"

    # model inheritance
    # Extension  add fields or methods to an existing model
    property_id = fields.Many2one("property")

    # python inheritance
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        print("Inside action confirm")
        return res
