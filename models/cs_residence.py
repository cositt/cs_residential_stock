from odoo import _, api, fields, models
from odoo.exceptions import UserError


class CsResidence(models.Model):
    _inherit = "cs.residence"

    @api.model
    def _resolve_stock_warehouse(self):
        """Almacén de la compañía activa, o el primero accesible por el usuario."""
        Warehouse = self.env["stock.warehouse"]
        wh = Warehouse.search([("company_id", "=", self.env.company.id)], limit=1)
        if wh:
            return wh
        return Warehouse.search(
            [("company_id", "in", self.env.user.company_ids.ids)], limit=1
        )

    @api.model
    def _stock_warehouse_available(self):
        return bool(self._resolve_stock_warehouse())

    stock_location_id = fields.Many2one(
        "stock.location",
        string="Ubicación de stock de la residencia",
        readonly=True,
        copy=False,
        groups="stock.group_stock_user",
        help="Ubicación interna bajo «Almacenes residenciales». Los movimientos de inventario "
        "cuentan aquí el stock consolidado de la residencia (incluye habitaciones).",
        ondelete="restrict",
    )

    @api.model
    def _get_or_create_residential_stock_root(self):
        """Raíz común: hijo directo del stock principal del almacén resuelto."""
        warehouse = self._resolve_stock_warehouse()
        if not warehouse:
            raise UserError(
                _(
                    "No hay ningún almacén de inventario disponible (compañía actual ni compañías "
                    "a las que tiene acceso). Cree un almacén en Inventario antes de usar "
                    "Almacenes residenciales."
                )
            )
        company = warehouse.company_id
        parent = warehouse.lot_stock_id
        Location = self.env["stock.location"]
        root = Location.search(
            [
                ("location_id", "=", parent.id),
                ("usage", "=", "internal"),
                ("name", "=", "Almacenes residenciales"),
                ("company_id", "=", company.id),
            ],
            limit=1,
        )
        if not root:
            root = Location.create(
                {
                    "name": "Almacenes residenciales",
                    "usage": "internal",
                    "location_id": parent.id,
                    "company_id": company.id,
                }
            )
        return root

    def _residential_stock_location_name(self):
        self.ensure_one()
        return (self.code or self.name or "").strip() or _("Residencia")

    def _ensure_residential_stock_location(self):
        self.ensure_one()
        if self.stock_location_id:
            return self.stock_location_id
        if not self._stock_warehouse_available():
            raise UserError(
                _(
                    "No hay almacén para esta compañía. Configure Inventario (almacén) antes de "
                    "generar ubicaciones residenciales."
                )
            )
        root = self._get_or_create_residential_stock_root()
        loc = self.env["stock.location"].create(
            {
                "name": self._residential_stock_location_name(),
                "usage": "internal",
                "location_id": root.id,
                "company_id": root.company_id.id,
                "cs_residence_id": self.id,
            }
        )
        self.sudo().write({"stock_location_id": loc.id})
        return loc

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        if self._stock_warehouse_available():
            for rec in records:
                rec._ensure_residential_stock_location()
        return records

    def write(self, vals):
        res = super().write(vals)
        if {"name", "code"} & set(vals):
            for rec in self:
                if rec.stock_location_id:
                    rec.stock_location_id.sudo().write(
                        {"name": rec._residential_stock_location_name()}
                    )
        return res

    def action_generate_residential_stock_location(self):
        """Retrocompatibilidad o tras crear el primer almacén."""
        self.ensure_one()
        self._ensure_residential_stock_location()
        return True

    def action_open_residential_stock_quants(self):
        self.ensure_one()
        if not self.stock_location_id:
            raise UserError(
                _("Genere primero la ubicación de stock de esta residencia.")
            )
        return {
            "type": "ir.actions.act_window",
            "name": _("Existencias en residencia"),
            "res_model": "stock.quant",
            "view_mode": "list,pivot,form",
            "domain": [("location_id", "child_of", self.stock_location_id.id)],
            "context": {"group_by": ["location_id"]},
        }

    @api.model
    def action_menu_residential_stock_quants(self):
        """Desde menú: todas las cantidades bajo la raíz «Almacenes residenciales»."""
        root = self._get_or_create_residential_stock_root()
        return {
            "type": "ir.actions.act_window",
            "name": _("Existencias por ubicación"),
            "res_model": "stock.quant",
            "view_mode": "list,pivot,form",
            "domain": [("location_id", "child_of", root.id)],
            "context": {"group_by": ["location_id"]},
        }

    @api.model
    def action_menu_residential_locations(self):
        root = self._get_or_create_residential_stock_root()
        return {
            "type": "ir.actions.act_window",
            "name": _("Ubicaciones residenciales"),
            "res_model": "stock.location",
            "view_mode": "list,form",
            "domain": [("id", "child_of", root.id)],
            "context": {},
        }
