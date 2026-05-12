from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    cs_resident_id = fields.Many2one(
        "cs.resident",
        string="Residente (por defecto líneas)",
        tracking=True,
        help="Se propaga a las líneas de movimiento si están vacías (al confirmar / validar).",
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
        string="Zona limpieza (por defecto líneas)",
        tracking=True,
    )
    cs_responsible_signature = fields.Binary(
        string="Firma responsable (por defecto líneas)",
        attachment=True,
    )

    def _cs_propagate_residential_to_moves(self):
        """Repite datos del albarán en movimientos que aún no los tienen."""
        for picking in self:
            for move in picking.move_ids:
                vals = {}
                if picking.cs_resident_id and not move.cs_resident_id:
                    vals["cs_resident_id"] = picking.cs_resident_id.id
                if picking.cs_cleaning_zone and not move.cs_cleaning_zone:
                    vals["cs_cleaning_zone"] = picking.cs_cleaning_zone
                if picking.cs_responsible_signature and not move.cs_responsible_signature:
                    vals["cs_responsible_signature"] = picking.cs_responsible_signature
                if vals:
                    move.write(vals)

    @api.onchange("cs_resident_id", "cs_cleaning_zone", "cs_responsible_signature")
    def _onchange_cs_residential_header(self):
        for move in self.move_ids:
            if self.cs_resident_id:
                move.cs_resident_id = self.cs_resident_id
            if self.cs_cleaning_zone:
                move.cs_cleaning_zone = self.cs_cleaning_zone
            if self.cs_responsible_signature:
                move.cs_responsible_signature = self.cs_responsible_signature

    def action_confirm(self):
        res = super().action_confirm()
        self._cs_propagate_residential_to_moves()
        return res

    def button_validate(self):
        self._cs_propagate_residential_to_moves()
        return super().button_validate()
