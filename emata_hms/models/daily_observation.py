from odoo import _, api, fields, models, exceptions, tools

   
class EmHmsDailyObservation(models.Model):
    _name = 'em.hms.daily.observation'
    _description = 'Daily Observation'
    _rec_name = 'patient_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    incubator_admission_id = fields.Many2one('em.hms.pediatric.incubator.admission', string='Incubator Admission')
    ward_admission_id = fields.Many2one('em.hms.pediatric.ward.admission', string='Ward Admission')
    pediatric_surgery_id = fields.Many2one('em.hms.pediatric.surgery', string='Pediatric Surgery')
    icu_id = fields.Many2one('em.hms.pediatric.icu', string='ICU')
    nicu_id = fields.Many2one('em.hms.pediatric.nicu', string='NICU')
    patient_id = fields.Many2one('res.partner', 'Patient Name', required=True, domain=[('is_patient','=',True)])
    
    viewing_datetime = fields.Date('Viewing Date/Time', tracking=True)
    testing_evaluation = fields.Char('Testing And Evaluation', tracking=True)
    oral_nutrition = fields.Integer('Oral Nutrition', tracking=True)
    responsible_nurse1_id = fields.Many2one('hr.employee', string='Responsible Nurse1', tracking=True)
    responsible_nurse2_id = fields.Many2one('hr.employee', string='Responsible Nurse2', tracking=True)
    resident_doctor_id = fields.Many2one('hr.employee', string='Resident Doctor', tracking=True)
    specialist_doctor_id = fields.Many2one('hr.employee', string='Specialist Doctor', tracking=True)
    
    company_id = fields.Many2one('res.company', 'Medical Center', default = lambda self: self.env.company)
    
    @api.onchange('incubator_admission_id')
    def _onchange_incubator_admission_id(self):
        if self.incubator_admission_id:
            self.patient_id = self.incubator_admission_id.patient_id.id
            
    @api.onchange('ward_admission_id')
    def _onchange_ward_admission_id(self):
        if self.ward_admission_id:
            self.patient_id = self.ward_admission_id.patient_id.id
            
    @api.onchange('pediatric_surgery_id')
    def _onchange_pediatric_surgery_id(self):
        if self.pediatric_surgery_id:
            self.patient_id = self.pediatric_surgery_id.patient_id.id
            
    @api.onchange('icu_id')
    def _onchange_icu_id(self):
        if self.icu_id:
            self.patient_id = self.icu_id.patient_id.id
            
    @api.onchange('nicu_id')
    def _onchange_nicu_id(self):
        if self.nicu_id:
            self.patient_id = self.nicu_id.patient_id.id
            

            
    