from odoo import _, api, fields, models, exceptions, tools

BLOOD_TYPES = [
    ('A+', 'A+'),
    ('B+', 'B+'),
    ('O+', 'O+'),
    ('AB+', 'AB+'),
    ('A-', 'A-'),
    ('B-', 'B-'),
    ('O-', 'O-'),
    ('AB-', 'AB-')
]

class EmHmsChildCare(models.Model):
    _name = 'em.hms.child.care'
    _description = 'Child Care'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Name', required=True, tracking=True)
    name_lang = fields.Char('Arabic Name', tracking=True)


class EmHmsPediatricNewbornExamination(models.Model):
    _name = 'em.hms.pediatric.newborn.examination'
    _description = 'Newborn Examination'
    _rec_name = 'patient_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    patient_id = fields.Many2one('res.partner', 'Patient Name', required=True, domain=[('is_patient','=',True)])
    examination_datetime = fields.Datetime('Admission Date/Time', required=True, tracking=True)
    gestational_weeks_count = fields.Integer('Number Of Gestational Weeks', tracking=True)
    weight = fields.Float('Weight (kg)', tracking=True)
    height = fields.Float('Height (cm)', tracking=True)
    cranial_circumference = fields.Integer('Cranial Circumference', tracking=True)
    birth_date = fields.Date('Birth Date', required=True, tracking=True)
    birth_type = fields.Selection([
        ('normal', 'Normal'),
        ('cesarean_section', 'Cesarean Section')
    ], string='Type Of Birth', tracking=True)
    child_care_ids = fields.Many2many('em.hms.child.care', 'newborn_examination_child_care_rel', 'newborn_examination_id', 'child_care_id', string='Routine Child Care')
    general_examination = fields.Char('General Examination Of The Child', tracking=True)
    graduation_to = fields.Selection([
        ('home', 'Home'),
        ('care', 'Care'),
        ('incubator', 'Incubator'),
        ('incubator_temporary', 'Temporary Monitoring In Incubator')
    ], string='Graduation To', tracking=True)
    graduation_date = fields.Date('Graduation Date', tracking=True)
    medical_recommendations = fields.Char('Medical Recommendations At Graduation', tracking=True)
    doctor_id = fields.Many2one('hr.employee', string='Doctor', tracking=True)
    nurse_id = fields.Many2one('hr.employee', string='Nurse', tracking=True)
    
    company_id = fields.Many2one('res.company', 'Medical Center', default = lambda self: self.env.company)
    
    _sql_constraints = [
        (
            'check_examination_datetime',
            'CHECK (examination_date <= NOW())',
            'Examination Date/Time Must Not Be Newer Than Now.'
        ),
        (
            'check_birth_date',
            'CHECK (birth_date <= CURRENT_DATE)',
            'Birth Date Must Not Be Newer Than Today.'
        ),
        (
            'check_graduation_date',
            'CHECK (graduation_date <= CURRENT_DATE)',
            'Graduation Date Must Not Be Newer Than Today.'
        ),
    ]

