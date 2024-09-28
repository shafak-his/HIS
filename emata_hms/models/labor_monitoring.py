from odoo import _, api, fields, models, exceptions, tools

   
class EmHmsRHSLabor(models.Model):
    _name = 'em.hms.labor'
    _description = 'Labor Monitoring'
    _rec_name = 'activity_name'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    delivery_id = fields.Many2one('em.hms.rhs.delivery', string='Delivery')
    hospitalization_id = fields.Many2one('em.hms.rhs.hospitalization', string='Hospitalization')
    surgery_id = fields.Many2one('em.hms.rhs.surgery', string='Surgery')
    patient_id = fields.Many2one('res.partner', 'Patient Name', required=True, domain=[('is_patient','=',True)])
    
    activity_name = fields.Char('Activity', tracking=True)
    labor_hour = fields.Datetime('Hour', tracking=True)
    contraction_duration = fields.Float('Contraction Duration', tracking=True)
    interval_between_contractions = fields.Float('Interval Between Contractions', tracking=True)
    labor_auscultation = fields.Char('Labor Auscultation', tracking=True)
    dilation = fields.Float('Dilation', tracking=True)
    erasure = fields.Float('Erasure', tracking=True)
    
    company_id = fields.Many2one('res.company', 'Medical Center', default = lambda self: self.env.company)
    
    @api.onchange('delivery_id')
    def _onchange_delivery_id(self):
        if self.delivery_id:
            self.patient_id = self.delivery_id.patient_id.id
            self.activity_name = 'Delivery'
            
    @api.onchange('hospitalization_id')
    def _onchange_hospitalization_id(self):
        if self.hospitalization_id:
            self.patient_id = self.hospitalization_id.patient_id.id
            self.activity_name = 'Hospitalization'
            
    @api.onchange('surgery_id')
    def _onchange_surgery_id(self):
        if self.surgery_id:
            self.patient_id = self.surgery_id.patient_id.id
            self.activity_name = 'Surgery'
    