from odoo import _, api, fields, models, exceptions, tools


class EmHmsNecessityGiving(models.Model):
    _name = 'em.hms.necessity.giving'
    _description = 'Necessity Giving'
    _rec_name = 'patient_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    patient_admission_id = fields.Many2one('em.hms.patient.admission', string='Patient Admission') # , required=True
    hospitalization_id = fields.Many2one('em.hms.rhs.hospitalization', string='Hospitalization')
    incubator_admission_id = fields.Many2one('em.hms.pediatric.incubator.admission', string='Incubator Admission')
    ward_admission_id = fields.Many2one('em.hms.pediatric.ward.admission', string='Ward Admission')
    pediatric_surgery_id = fields.Many2one('em.hms.pediatric.surgery', string='Pediatric Surgery')
    pediatric_clinic_id = fields.Many2one('em.hms.pediatric.clinic', string='Pediatric Clinic')
    phototherapy_id = fields.Many2one('em.hms.pediatric.phototherapy', string='Phototherapy')
    icu_id = fields.Many2one('em.hms.pediatric.icu', string='ICU')
    nicu_id = fields.Many2one('em.hms.pediatric.nicu', string='NICU')
    patient_id = fields.Many2one('res.partner', 'Patient Name', required=True, domain=[('is_patient','=',True)])
    
    commitment_datetime = fields.Datetime('Necessity Giving Date/Time', required=True, tracking=True)
    doctor_id = fields.Many2one('hr.employee', 'Doctor', related='patient_admission_id.doctor_id')
    
    necessity_id = fields.Many2one('em.hms.daily.necessity', string='Daily Necessity',  tracking=True)
    # medication_request_id = fields.Many2one('em.hms.medication.request', string='Medication Name', related='necessity_id.medication_request_id')
    medication_id = fields.Many2one('product.template', string='Medication', related='necessity_id.medication_id')
    dosage = fields.Char('Dosage', related='necessity_id.dosage')
    rate = fields.Char('Rate', related='necessity_id.rate')
    dose_taking_way = fields.Selection([
        ('oral', 'Oral'),
        ('muscular', 'Muscular'),
        ('intravenous', 'Intravenous'),
        ('subcutaneous', 'Subcutaneous'),
        ('topical', 'Topical'),
        ('anal', 'Anal'),
        ('vaginal', 'Vaginal')
    ], string='Dose Taking Way', related='necessity_id.dose_taking_way')
    notes = fields.Char('Notes', tracking=True)
    
    company_id = fields.Many2one('res.company', 'Medical Center', default = lambda self: self.env.company)
    
    _sql_constraints = [
        (
            'check_commitment_datetime',
            'CHECK (commitment_datetime <= NOW())',
            'Necessity Giving Date/Time Must Not Be Newer Than Now.'
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



