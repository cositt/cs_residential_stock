{
    'name': 'Centro Sanitario - Stock residencial (Inventario)',
    'version': '19.0.1.2.0',
    'category': 'Healthcare',
    'summary': 'Extiende Inventario Odoo: ubicaciones por residencia/habitación, almacenes residenciales, '
                'clasificación Equilibrium, residente y firma en movimientos/albaranes.',
    'author': 'Equilibrium Dev Team',
    'license': 'LGPL-3',
    'depends': [
        'stock',
        'mail',
        'cs_resident',
    ],
    'data': [
        'security/record_rules.xml',
        'views/product_template_views.xml',
        'views/stock_move_views.xml',
        'views/stock_picking_views.xml',
        'views/residential_stock_residence_views.xml',
        'views/residential_stock_room_views.xml',
        'views/residential_stock_location_views.xml',
        'views/residential_warehouse_menus.xml',
        'views/menu_items.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'post_init_hook': 'post_init_hook',
}
