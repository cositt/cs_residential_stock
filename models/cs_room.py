from odoo import _, api, fields, models
from odoo.exceptions import UserError


class CsRoom(models.Model):
    _inherit = "cs.room"

    stock_location_id = fields.Many2one(
        "stock.location",
        string="Ubicación de stock de la habitación",
        readonly=True,
        copy=False,
        groups="stock.group_stock_user",
        help="Ubicación interna hija de la ubicación de la residencia. Use transferencias internas "
        "para repartir productos entre habitaciones.",
        ondelete="restrict",
    )

    def _room_stock_location_name(self):
        self.ensure_one()
        base = (self.name or "").strip() or _("Habitación")
        res_code = (
            (self.residence_id.code or self.residence_id.name or "").strip() or ""
        )
        return " / ".join(p for p in (res_code, base) if p)

    def _ensure_residential_stock_location(self):
        self.ensure_one()
        if self.stock_location_id:
            return self.stock_location_id
        if not self.residence_id:
            raise UserError(_("La habitación debe tener una residencia."))
        parent_loc = self.residence_id._ensure_residential_stock_location()
        loc = self.env["stock.location"].create(
            {
                "name": self._room_stock_location_name(),
                "usage": "internal",
                "location_id": parent_loc.id,
                "company_id": parent_loc.company_id.id,
                "cs_residence_id": self.residence_id.id,
                "cs_room_id": self.id,
            }
        )
        self.sudo().write({"stock_location_id": loc.id})
        return loc

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        if self.env["cs.residence"]._stock_warehouse_available():
            for rec in records:
                rec._ensure_residential_stock_location()
        return records

    def write(self, vals):
        if (
            "residence_id" in vals
            and not self.env.context.get("cs_skip_room_residence_guard")
        ):
            for room in self:
                if (
                    room.stock_location_id
                    and vals["residence_id"] != room.residence_id.id
                ):
                    raise UserError(
                        _(
                            "No puede cambiar la residencia de una habitación que ya tiene ubicación "
                            "de stock. Vacíe el stock o archive la habitación y cree una nueva."
                        )
                    )
        res = super().write(vals)
        if "name" in vals:
            for rec in self:
                if rec.stock_location_id:
                    rec.stock_location_id.sudo().write(
                        {"name": rec._room_stock_location_name()}
                    )
        return res

    def action_generate_room_stock_location(self):
        self.ensure_one()
        self._ensure_residential_stock_location()
        return True

    def action_open_room_stock_quants(self):
        self.ensure_one()
        if not self.stock_location_id:
            raise UserError(
                _("Genere primero la ubicación de stock de esta habitación.")
            )
        return {
            "type": "ir.actions.act_window",
            "name": _("Existencias en habitación"),
            "res_model": "stock.quant",
            "view_mode": "list,pivot,form",
            "domain": [("location_id", "child_of", self.stock_location_id.id)],
            "context": {"group_by": ["location_id"]},
        }
