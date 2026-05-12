{
    'name': 'Centro Sanitario - Stock residencial (Inventario)',
    'version': '19.0.1.0.0',
    'category': 'Healthcare',
    'summary': 'Extiende Inventario Odoo: clasificación Equilibrium, residente, zona limpieza y firma en movimientos/albaranes.',
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
        'views/menu_items.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
