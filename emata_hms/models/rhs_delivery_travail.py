from odoo import _, api, fields, models, exceptions, tools


class EmHmsRHSDeliveryTravail(models.Model):
    _name = 'em.hms.rhs.delivery.travail'
    _description = 'Delivery Travail'
    _rec_name = 'delivery_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    delivery_id = fields.Many2one('em.hms.rhs.delivery', string='Delivery', required=True)
    patient_id = fields.Many2one('res.partner', 'Patient Name', related='delivery_id.patient_id')
    travail_hour = fields.Datetime('Hour', required=True, tracking=True)
    contraction_duration = fields.Float('Contraction Duration', required=True, tracking=True)
    interval_between_contractions = fields.Float('Interval Between Contractions', required=True, tracking=True)
    travail_auscultation = fields.Char('Travail Auscultation', required=True, tracking=True)
    dilation = fields.Float('Dilation', required=True, tracking=True)
    erasure = fields.Float('Erasure', required=True, tracking=True)
    
    company_id = fields.Many2one('res.company', 'Medical Center', default = lambda self: self.env.company)
    