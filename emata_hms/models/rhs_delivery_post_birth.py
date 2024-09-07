from odoo import _, api, fields, models, exceptions, tools


class EmHmsRHSDeliveryPostBirth(models.Model):
    _name = 'em.hms.rhs.delivery.post.birth'
    _description = 'Post-Birth Monitoring'
    _rec_name = 'delivery_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    delivery_id = fields.Many2one('em.hms.rhs.delivery', string='Delivery', required=True)
    patient_id = fields.Many2one('res.partner', 'Patient Name', related='delivery_id.patient_id')
    datetime = fields.Datetime('Time', required=True, tracking=True)
    pressure = fields.Integer('Pressure', tracking=True)
    pulse = fields.Integer('Pulse', tracking=True)
    temperature = fields.Float('Temperature', tracking=True)
    is_safety_ball = fields.Boolean('Safety Ball', tracking=True)
    is_urine_voiding = fields.Boolean('Urine Voiding', tracking=True)
    notes = fields.Char('Notes')
    
    company_id = fields.Many2one('res.company', 'Medical Center', default = lambda self: self.env.company)

    