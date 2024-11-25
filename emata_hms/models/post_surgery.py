from odoo import _, api, fields, models, exceptions, tools


class EmHmsRHSDeliveryPostBirth(models.Model):
    _name = 'em.hms.post.surgery'
    _description = 'Post-Surgery Monitoring'
    _rec_name = 'activity_name'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    patient_id = fields.Many2one('res.partner', 'Patient Name', required=True, domain=[('is_patient','=',True)])
    datetime = fields.Datetime('Time', required=True, tracking=True)
    activity_name = fields.Char('Activity', tracking=True)
    delivery_id = fields.Many2one('em.hms.rhs.delivery', string='Delivery')
    surgery_id = fields.Many2one('em.hms.rhs.surgery', string='Surgery')
    
    pressure = fields.Integer('Pressure', tracking=True)
    pulse = fields.Integer('Pulse', tracking=True)
    temperature = fields.Float('Temperature', tracking=True)
    is_safety_ball = fields.Boolean('Safety Ball', tracking=True)
    is_urine_voiding = fields.Boolean('Urine Voiding', tracking=True)
    drainage_result = fields.Integer('Drainage Result', tracking=True)
    notes = fields.Char('Notes')
    
    company_id = fields.Many2one('res.company', 'Medical Center', default = lambda self: self.env.company)
    
    @api.onchange('delivery_id')
    def _onchange_delivery_id(self):
        if self.delivery_id:
            self.patient_id = self.delivery_id.patient_id.id
            self.activity_name = 'Delivery'
            
    @api.onchange('surgery_id')
    def _onchange_surgery_id(self):
        if self.surgery_id:
            self.patient_id = self.surgery_id.patient_id.id
            self.activity_name = 'Surgery'

    