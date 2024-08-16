from odoo import _, api, fields, models, exceptions, tools


class EmHmsRHSDeliveryBirth(models.Model):
    _name = 'em.hms.rhs.delivery.birth'
    _description = 'Delivery Post-Birth'
    _rec_name = 'delivery_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    delivery_id = fields.Many2one('em.hms.rhs.delivery', string='Delivery', required=True)
    patient_id = fields.Many2one('res.partner', 'Patient Name', related='delivery_id.patient_id')
    post_birth_datetime = fields.Datetime('Time', required=True, tracking=True)
    post_birth_pressure = fields.Integer('Pressure', required=True, tracking=True)
    post_birth_pulse = fields.Integer('Pulse', required=True, tracking=True)
    post_birth_temperature = fields.Float('Temperature', required=True, tracking=True)
    is_post_birth_safety_ball = fields.Boolean('Safety Ball', tracking=True)
    is_post_birth_urine_voiding = fields.Boolean('Urine Voiding', tracking=True)
    post_birth_notes = fields.Char('Notes')
    
    company_id = fields.Many2one('res.company', 'Medical Center', default = lambda self: self.env.company)
    