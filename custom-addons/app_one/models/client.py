from odoo import models, fields


# model inheritance
class Clinet(models.Model):
    # Classical inheritance creates a new model that inherits fields and methods from a parent model
    _name = "client"
    _inherit = "owner"
