from odoo import _, api, fields, models, exceptions, tools


class EmHmsDailyNecessity(models.Model):
    _name = 'em.hms.daily.necessity'
    _description = 'Daily Necessity'
    _rec_name = 'activity_name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    patient_admission_id = fields.Many2one('em.hms.patient.admission', string='Patient Admission')
    hospitalization_id = fields.Many2one('em.hms.rhs.hospitalization', string='Hospitalization')
    activity_name = fields.Char('Activity', tracking=True)
    
    necessity_datetime = fields.Datetime('Necessity Date/Time', required=True, tracking=True)
    patient_id = fields.Many2one('res.partner', 'Patient Name', required=True, domain=[('is_patient','=',True)])
    doctor_id = fields.Many2one('hr.employee', 'Doctor', related='patient_admission_id.doctor_id')
    ward_nurse_id = fields.Many2one('hr.employee', string='Name Of The Ward Nurse', tracking=True)
    
    # medication_request_id = fields.Many2one('em.hms.medication.request', string='Medication Name', tracking=True)
    medication_id = fields.Many2one('product.template', string='Product', domain="[('is_medication', '=', True)]", required=True)
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
            self.activity_name = 'Patient Admission'
            
    @api.onchange('hospitalization_id')
    def _onchange_hospitalization_id(self):
        if self.hospitalization_id:
            self.patient_id = self.hospitalization_id.patient_id.id
            self.activity_name = 'Hospitalization'


