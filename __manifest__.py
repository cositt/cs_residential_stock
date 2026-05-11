{
    'name': 'Centro Sanitario - Gestión de Stock Residencial',
    'version': '1.0.0',
    'category': 'Healthcare',
    'summary': 'Módulo simple para control de suplidos, comida, limpieza y material sanitario',
    'author': 'Equilibrium Dev Team',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'mail',
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/record_rules.xml',
        'data/ir_sequence.xml',
        'views/cs_stock_movement_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
