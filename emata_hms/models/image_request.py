from odoo import _, api, fields, models, exceptions, tools

class EmHmsImageRequest(models.Model):
    _name = 'em.hms.image.request'
    _description = 'Image Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    general_visit_id = fields.Many2one('em.hms.general.clinic.visit', string='General Visit')
    gynochological_visit_id = fields.Many2one('em.hms.gynochological.clinic.visit', string='Gynochological Visit')
    pnc_visit_id = fields.Many2one('em.hms.rhs.pnc.visit', string='PNC Visit')
    dial_urology_id = fields.Many2one('em.hms.dial.urology', string='Urology Visit')
    dial_nephrology_id = fields.Many2one('em.hms.dial.nephrology', string='Nephrology Visit')

    product_template_id = fields.Many2one('product.template', string='Product', domain="[('is_medical_imaging', '=', True)]", required=True)
    notes = fields.Char('Notes')