from odoo.exceptions import ValidationError

from odoo import api, fields, models


class property(models.Model):
    _name = "property"

    name = fields.Char(required=1, default="New", size=10)
    description = fields.Text()
    postcode = fields.Char(required=1)
    date_availability = fields.Date()
    expected_price = fields.Float()
    selling_price = fields.Float()
    diff = fields.Float(compute="_compute_diff", store=1, readonly=0)
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    owner_id = fields.Many2one("owner")
    garden_orientation = fields.Selection(
        [
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        default="north",
    )
    tag_ids = fields.Many2many("tag")
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("pending", "Pending"),
            ("sold", "Sold"),
        ],
        default="draft",
    )

    _sql_constraints = [  # noqa: RUF012
        # constraint name , constraint(column), error message
        ("unique_name", "unique(name)", "This name exists")
    ]

    @api.constrains("bedrooms")
    def _check_bedrooms(self):
        for rec in self:
            if rec.bedrooms <= 0:
                raise ValidationError("Please add a valid value")

    def action_draft(self):
        for rec in self:
            rec.state = "draft"

    def action_pending(self):
        for rec in self:
            rec.state = "pending"

    def action_sold(self):
        for rec in self:
            rec.state = "sold"

    # it can be triggred from the local fields views and other realtion
    # returns real record
    @api.depends("expected_price", "selling_price", "owner_id.phone")
    def _compute_diff(self):
        for rec in self:
            rec.diff = rec.expected_price - rec.selling_price

    # it can be triggred from the local fields views
    # returns sudeo record
    @api.onchange("expected_price")
    def _onchange_expected_price(self):
        for rec in self:
            print("inside onchange")

            return {
                "warning": {
                    "title": "warning",
                    "message": "negative value",
                    "type": "notification",
                }
            }

    # # Create
    # @api.model_create_multi
    # def create(self, vals):
    #     res = super().create(vals)
    #     print("Inside create method ")
    #     return res

    # # Read
    # @api.model
    # def _search(self, domain, offset=0, limit=None, order=None, access_rights_uid=None):
    #     res = super()._search(
    #         domain, offset=0, limit=None, order=None, access_rights_uid=None
    #     )

    #     print("Inside Read")
    #     return res

    # # Update
    # def write(self, vals):
    #     res = super().write(vals)
    #     print("Inside Write")
    #     return res

    # # Delete
    # def unlink(self):
    #     res = super().unlink()
    #     print("Inside Delete")
    #     return res
