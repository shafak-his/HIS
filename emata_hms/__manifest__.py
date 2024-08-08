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

    'depends': ['base', 'mail'],

    'data': [
        'security/ir.model.access.csv',

        'views/phc_clinic_visit_view.xml',
        'views/phc_clinic_view.xml',
        'views/phc_icd10_view.xml',
        'views/mh_referral_view.xml',
        
        'views/menus_view.xml',
    ],
}
