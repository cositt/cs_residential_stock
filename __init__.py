from . import models


def post_init_hook(env):
    Res = env["cs.residence"]
    if not Res._stock_warehouse_available():
        return
    Res._get_or_create_residential_stock_root()
    for residence in env["cs.residence"].search([]):
        if not residence.stock_location_id:
            residence._ensure_residential_stock_location()
    for room in env["cs.room"].search([]):
        if not room.stock_location_id:
            room._ensure_residential_stock_location()
