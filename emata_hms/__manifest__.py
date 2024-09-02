{
    'name': "Emata HMS",

    'summary': 'Emata HMS',

    'description': '',

    'author': "Emata",
    'website': "https://emata.com.tr",
    'category': 'Tools',
    'version': '17.0.0.0',
    'application': True,
    'sequence': 1,
    'installable': True,

    'depends': [
        'base',
        'mail',
        'product',
        'hr',
        'web_responsive',
        'web_m2x_options',
        'disable_odoo_online'
    ],

    'data': [
        'security/ir.model.access.csv',

        'views/phc_clinic_visit_view.xml',
        'views/clinic_view.xml',
        'views/icd10_view.xml',
        'views/mh_referral_view.xml',
        'views/mh_gap_view.xml',
        'views/mh_awareness_view.xml',
        'views/mh_pmplus_view.xml',
        'views/rhs_anc_view.xml',
        'views/rhs_anc_visit_view.xml',
        'views/rhs_pnc_view.xml',
        'views/rhs_pnc_visit_view.xml',
        'views/rhs_delivery_view.xml',
        'views/rhs_delivery_labor_view.xml',
        'views/rhs_delivery_post_birth_view.xml',
        'views/vital_signs_view.xml',
        'views/master_models_view.xml',
        'views/res_partner_view.xml',
        'views/product_template_view.xml',
        'views/dial_nephrology_view.xml',
        'views/dial_urology_view.xml',
        'views/dial_lithotripsy_view.xml',
        'views/dial_prescription_view.xml',
        'views/dial_kidney_history_view.xml',
        'views/dial_visit_view.xml',
        'views/nutrition_group_session.xml',

        'data/sequence_data.xml',

        'views/menus_view.xml',
    ],
}
