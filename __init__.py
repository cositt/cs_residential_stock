from odoo import api
from odoo.api import SUPERUSER_ID

from . import models


def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    companies = env["res.company"].search([])
    for company in companies:
        cenv = env.with_company(company)
        Res = cenv["cs.residence"]
        if not Res._stock_warehouse_available():
            continue
        Res._get_or_create_residential_stock_root()
        for residence in cenv["cs.residence"].search([]):
            if not residence.stock_location_id:
                residence._ensure_residential_stock_location()
        for room in cenv["cs.room"].search([]):
            if not room.stock_location_id:
                room._ensure_residential_stock_location()
