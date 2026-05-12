from odoo import fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    cs_residential_category = fields.Selection(
        related="product_id.product_tmpl_id.cs_residential_supply_category",
        string="Categoría residencial",
        store=True,
        readonly=True,
    )
    cs_resident_id = fields.Many2one(
        "cs.resident",
        string="Residente (consumo/asignación)",
        tracking=True,
        help="Opcional: vincula el movimiento a un residente concreto.",
    )
    cs_cleaning_zone = fields.Selection(
        selection=[
            ("kitchen", "Cocina"),
            ("bathrooms", "Baños"),
            ("rooms", "Habitaciones"),
            ("laundry", "Lavandería"),
            ("dining", "Comedor"),
            ("other", "Otros"),
        ],
        string="Zona (limpieza)",
        tracking=True,
        help="Suele usarse cuando la categoría residencial del producto es limpieza.",
    )
    cs_responsible_signature = fields.Binary(
        string="Firma del responsable",
        attachment=True,
        help="Captura o archivo de firma para auditoría del movimiento.",
    )
