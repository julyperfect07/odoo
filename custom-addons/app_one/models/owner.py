from odoo import fields, models


class Owner(models.Model):
    _name = "owner"

    name = fields.Char(required=True)
    phone = fields.Char()
    address = fields.Char()
    propery_ids = fields.One2many("property", "owner_id")

    # the sql constraints doesnt apply if there were records that contradicts it
    _sql_constraints = [  # noqa: RUF012
        # constraint name , constraint(column), error message
        ("unique_name", "unique(name)", "This name exists")
    ]
