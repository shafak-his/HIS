from odoo import _, api, fields, models, exceptions, tools


# General, Bone, etc...
SURGICAL_CATEGORIES = [
    ('general', 'General'),
    ('bone', 'Bone'),
    ('delivery', 'Delivery'),
    ('gynecological', 'Gynecological'),
    ('pediatric', 'Pediatric'),
    ('respiratory', 'Respiratory'),
    ('digestive', 'Digestive'),
    ('internal', 'Internal'),
    ('neurological', 'Neurological'),
    ('infectious', 'Infectious')
]

# (صغرى	الفتوق	افات الشرج	جراحة البطن	أخرى عمليات عظمية كبرى	عظمية صغرى), etc...
class EmHmsSurgicalSubCategory(models.Model): 
    _name = 'em.hms.surgical.subcategory'
    _description = 'Surgical Sub-Category'
    _rec_name = 'name'

    name = fields.Char('Name', required=True)
    name_lang = fields.Char('Arabic Name', required=True)
    category = fields.Selection(SURGICAL_CATEGORIES, string='Category', required=True)
    

class EmHmsSurgicalProcedure(models.Model):
    _name = 'em.hms.surgical.procedure'
    _description = 'Surgical Procedure'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char('Name', required=True)
    name_lang = fields.Char('Arabic Name', required=True)
    subcategory_id = fields.Many2one('em.hms.surgical.subcategory', string='Sub-Category', required=True)
    category = fields.Selection(SURGICAL_CATEGORIES, string='Category', related='subcategory_id.category')
