{
    'name': "Odoo Sponsorship module for Easy My Coop cooperative addons",
    'version': '12.0.0.0.1',
    'depends': ['easy_my_coop'],
    'author': "Coopdevs Treball SCCL",
    'website': 'https://coopdevs.org',
    'category': "Cooperative management",
    'description': """
    Odoo Sponsorship module for Easy My Coop cooperative addons.
    """,
    "license": "AGPL-3",
    'data': [
        'views/subscription_request_view.xml',
        'views/res_partner_view.xml',
        'wizard/sponsee_member_wizard.xml',
        'views/menus.xml',
    ],
}
