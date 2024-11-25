from odoo import _, api, fields, models, exceptions, tools


class EmHmsDailyNecessity(models.Model):
    _name = 'em.hms.daily.necessity'
    _description = 'Daily Necessity'
    _rec_name = 'patient_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    patient_admission_id = fields.Many2one('em.hms.patient.admission', string='Patient Admission')
    hospitalization_id = fields.Many2one('em.hms.rhs.hospitalization', string='Hospitalization')
    incubator_admission_id = fields.Many2one('em.hms.pediatric.incubator.admission', string='Incubator Admission')
    ward_admission_id = fields.Many2one('em.hms.pediatric.ward.admission', string='Ward Admission')
    pediatric_surgery_id = fields.Many2one('em.hms.pediatric.surgery', string='Pediatric Surgery')
    pediatric_clinic_id = fields.Many2one('em.hms.pediatric.clinic', string='Pediatric Clinic')
    phototherapy_id = fields.Many2one('em.hms.pediatric.phototherapy', string='Phototherapy')
    icu_id = fields.Many2one('em.hms.pediatric.icu', string='ICU')
    nicu_id = fields.Many2one('em.hms.pediatric.nicu', string='NICU')
    patient_id = fields.Many2one('res.partner', 'Patient Name', required=True, domain=[('is_patient','=',True)])
    
    necessity_datetime = fields.Datetime('Necessity Date/Time', required=True, tracking=True)
    doctor_id = fields.Many2one('hr.employee', 'Doctor', related='patient_admission_id.doctor_id')
    ward_nurse_id = fields.Many2one('hr.employee', string='Name Of The Ward Nurse', tracking=True)
    
    medication_id = fields.Many2one('product.template', string='Medication', domain="[('is_medication', '=', True)]", required=True)
    dosage = fields.Char('Dosage', tracking=True)
    rate = fields.Char('Rate', tracking=True)
    dose_taking_way = fields.Selection([
        ('oral', 'Oral'),
        ('muscular', 'Muscular'),
        ('intravenous', 'Intravenous'),
        ('subcutaneous', 'Subcutaneous'),
        ('topical', 'Topical'),
        ('anal', 'Anal'),
        ('vaginal', 'Vaginal')
    ], string='Dose Taking Way', tracking=True)
    doctor_id = fields.Many2one('hr.employee', string='Responsible Doctor', tracking=True)
    
    company_id = fields.Many2one('res.company', 'Medical Center', default = lambda self: self.env.company)
    
    _sql_constraints = [
        (
            'check_necessity_datetime',
            'CHECK (necessity_datetime <= NOW())',
            'Necessity Date/Time Must Not Be Newer Than Now.'
        ),
    ]
    
    @api.onchange('patient_admission_id')
    def _onchange_patient_admission_id(self):
        if self.patient_admission_id:
            self.patient_id = self.patient_admission_id.patient_id.id
            
    @api.onchange('hospitalization_id')
    def _onchange_hospitalization_id(self):
        if self.hospitalization_id:
            self.patient_id = self.hospitalization_id.patient_id.id
            
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
            
    @api.onchange('pediatric_clinic_id')
    def _onchange_pediatric_clinic_id(self):
        if self.pediatric_clinic_id:
            self.patient_id = self.pediatric_clinic_id.patient_id.id
            
    @api.onchange('phototherapy_id')
    def _onchange_phototherapy_id(self):
        if self.phototherapy_id:
            self.patient_id = self.phototherapy_id.patient_id.id
            
    @api.onchange('icu_id')
    def _onchange_icu_id(self):
        if self.icu_id:
            self.patient_id = self.icu_id.patient_id.id
            
    @api.onchange('nicu_id')
    def _onchange_nicu_id(self):
        if self.nicu_id:
            self.patient_id = self.nicu_id.patient_id.id


