from odoo import _, api, fields, models, exceptions, tools


class EmHmsVitalSign(models.Model):
    _name = 'em.hms.vital.sign'
    _description = 'Vital Signs'
    _rec_name = 'patient_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    delivery_id = fields.Many2one('em.hms.rhs.delivery', string='Delivery')
    hospitalization_id = fields.Many2one('em.hms.rhs.hospitalization', string='Hospitalization')
    surgery_id = fields.Many2one('em.hms.rhs.surgery', string='RHS Surgery')
    incubator_admission_id = fields.Many2one('em.hms.pediatric.incubator.admission', string='Incubator Admission')
    ward_admission_id = fields.Many2one('em.hms.pediatric.ward.admission', string='Ward Admission')
    pediatric_surgery_id = fields.Many2one('em.hms.pediatric.surgery', string='Pediatric Surgery')
    icu_id = fields.Many2one('em.hms.pediatric.icu', string='ICU')
    nicu_id = fields.Many2one('em.hms.pediatric.nicu', string='NICU')
    patient_admission_id = fields.Many2one('em.hms.patient.admission', string='Patient Admission')
    activity_name = fields.Char('Activity', tracking=True)
    patient_id = fields.Many2one('res.partner', 'Patient Name', required=True, domain=[('is_patient','=',True)])
    
    datetime = fields.Datetime('Time', required=True, tracking=True)
    pressure = fields.Float('Pressure', tracking=True)
    pulse = fields.Float('Pulse', tracking=True)
    oxygen = fields.Float('Oxygen', tracking=True)
    temperature = fields.Float('Temperature', tracking=True)
    awareness = fields.Char('Awareness', tracking=True)
    stool = fields.Float('Stool', tracking=True)
    urine = fields.Float('Urine', tracking=True)
    breathing = fields.Char('Breathing', tracking=True)
    cyan = fields.Char('Cyan', tracking=True)
    seizures = fields.Char('Seizures', tracking=True)
    vomiting = fields.Char('Vomiting', tracking=True)
    blood_sugar = fields.Float('Blood Sugar', tracking=True)
    feeding_type = fields.Selection([
        ('breastfeeding', 'Breastfeeding'),
        ('diverse_nutrition', 'Diverse nutrition'),
        ('ngt', 'NGT'),
        ('npo', 'NPO')
    ], string='Type Of Feeding', tracking=True)
    breastfeeding = fields.Float('Breastfeeding', tracking=True)
    ngt = fields.Float('NGT', tracking=True)
    explosives = fields.Char('Explosives', tracking=True)
    oral_intake = fields.Char('Oral Intake', tracking=True)
    hair_reed = fields.Float('Hair Reed', tracking=True)
    notes = fields.Char('Notes', tracking=True)

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
            self.activity_name = 'NICU'
    
    @api.onchange('patient_admission_id')
    def _onchange_patient_admission_id(self):
        if self.patient_admission_id:
            self.patient_id = self.patient_admission_id.patient_id.id
            self.activity_name = 'Patient Admission'
    
    
            

            