from odoo import _, api, fields, models, exceptions, tools

   
class EmHmsLaborMonitoring(models.Model):
    _name = 'em.hms.labor'
    _description = 'Labor Monitoring'
    _rec_name = 'patient_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    delivery_id = fields.Many2one('em.hms.rhs.delivery', string='Delivery')
    hospitalization_id = fields.Many2one('em.hms.rhs.hospitalization', string='Hospitalization')
    surgery_id = fields.Many2one('em.hms.rhs.surgery', string='Surgery')
    incubator_admission_id = fields.Many2one('em.hms.pediatric.incubator.admission', string='Incubator Admission')
    patient_id = fields.Many2one('res.partner', 'Patient Name', required=True, domain=[('is_patient','=',True)])
    
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
            
    @api.onchange('hospitalization_id')
    def _onchange_hospitalization_id(self):
        if self.hospitalization_id:
            self.patient_id = self.hospitalization_id.patient_id.id
            
    @api.onchange('surgery_id')
    def _onchange_surgery_id(self):
        if self.surgery_id:
            self.patient_id = self.surgery_id.patient_id.id
            
    @api.onchange('incubator_admission_id')
    def _onchange_incubator_admission_id(self):
        if self.incubator_admission_id:
            self.patient_id = self.incubator_admission_id.patient_id.id
    