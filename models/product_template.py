from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    cs_residential_supply_category = fields.Selection(
        selection=[
            ("food", "Comida"),
            ("cleaning", "Limpieza"),
            ("pharmacy", "Farmacia"),
            ("sanitary", "Material sanitario"),
            ("personal_hygiene", "Higiene personal"),
            ("other", "Otros"),
        ],
        string="Categoría suministro residencial",
        tracking=True,
        help="Clasificación para el almacén del centro residencial. Vacío = producto genérico sin clasificación Equilibrium.",
    )
