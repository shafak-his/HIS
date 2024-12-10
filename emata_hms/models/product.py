from odoo import _, api, fields, models, exceptions, tools


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    is_medication = fields.Boolean('Is Medication')
    is_medical_analysis = fields.Boolean('Is Medical Analysis')
    is_medical_imaging = fields.Boolean('Is Medical Imaging')
    is_birth_medication = fields.Boolean('Is Medication During Birth')
    is_surgery_medication = fields.Boolean('Is Medication During Surgery')

    # medication fields
    pharmaceutical_form = fields.Selection([
        ('tab', 'Tab'),
        ('flacon', 'Flacon'),
        ('amp', 'Amp'),
        ('vial', 'Vial'),
        ('btl', 'Btl'),
        ('pcs', 'Pcs'),
        ('tube', 'Tube'),
        ('supp', 'Supp'),
        ('bag', 'Bag'),
        ('spray', 'Spray'),
        ('sachet', 'Sachet'),
        ('cap', 'Cap'),
        ('jar', 'Jar'),
        ('pen', 'Pen'),
        ('kit', 'Kit'),
    ], string='Pharmaceutical Form')

    dosage_rate = fields.Selection([
        ('1x1', '1x1'),
        ('1x2', '1x2'),
        ('1x3', '1x3'),
        ('1x4', '1x4'),
        ('2x2', '2x2'),
        ('prn', 'PRN'),
    ], string='Dosage Rate')

    dose_time = fields.Selection([
        ('ac', 'A.C.'),
        ('bc', 'B.C.'),
    ], string='Dose Time')

    dose_way = fields.Selection([
        ('oral', 'Oral'),
        ('muscular', 'Muscular'),
        ('intravenous', 'Intravenous'),
        ('subcutaneous', 'Subcutaneous'),
        ('topical', 'Topical'),
        ('anal', 'Anal'),
        ('vaginal', 'Vaginal'),
    ], string='Dose Way')