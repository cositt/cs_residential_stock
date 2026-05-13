from odoo import fields, models


class StockLocation(models.Model):
    _inherit = "stock.location"

    cs_residence_id = fields.Many2one(
        "cs.residence",
        string="Residencia (Centro Sanitario)",
        index=True,
        ondelete="set null",
        copy=False,
    )
    cs_room_id = fields.Many2one(
        "cs.room",
        string="Habitación (Centro Sanitario)",
        index=True,
        ondelete="set null",
        copy=False,
    )
