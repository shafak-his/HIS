from odoo import _, api, fields, models, exceptions, tools


class EmHmsNecessityGiving(models.Model):
    _name = 'em.hms.necessity.giving'
    _description = 'Necessity Giving'
    _rec_name = 'activity_name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    patient_admission_id = fields.Many2one('em.hms.patient.admission', string='Patient Admission') # , required=True
    hospitalization_id = fields.Many2one('em.hms.rhs.hospitalization', string='Hospitalization')
    activity_name = fields.Char('Activity', tracking=True)
    
    commitment_datetime = fields.Datetime('Necessity Giving Date/Time', required=True, tracking=True)
    patient_id = fields.Many2one('res.partner', 'Patient Name', required=True, domain=[('is_patient','=',True)])
    doctor_id = fields.Many2one('hr.employee', 'Doctor', related='patient_admission_id.doctor_id')
    
    necessity_id = fields.Many2one('em.hms.daily.necessity', string='Daily Necessity',  tracking=True)
    # medication_request_id = fields.Many2one('em.hms.medication.request', string='Medication Name', related='necessity_id.medication_request_id')
    medication_id = fields.Many2one('product.template', string='Product', related='necessity_id.medication_id')
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
            self.activity_name = 'Patient Admission'
            
    @api.onchange('hospitalization_id')
    def _onchange_hospitalization_id(self):
        if self.hospitalization_id:
            self.patient_id = self.hospitalization_id.patient_id.id
            self.activity_name = 'Hospitalization'


