from odoo import _, api, fields, models, exceptions, tools


class EmHmsGynochologicalClinicVisit(models.Model):
    _name = 'em.hms.gynochological.clinic.visit'
    _description = 'Gynochological Clinic Visit'
    _rec_name = 'visit_datetime'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    visit_datetime = fields.Datetime('Visit Date/Time', required=True, tracking=True)
    patient_id = fields.Many2one('res.partner', string='Patient Name', required=True, domain=[('is_patient','=',True)], tracking=True)
    clinic_id = fields.Many2one('em.hms.clinic', string='Clinic Name', tracking=True)
    current_complaint = fields.Char('Current Complaint', tracking=True)
    diagnosis_id = fields.Many2one('em.hms.icd10', string='Diagnosis', tracking=True)
    procedures_followed = fields.Char('Procedures Followed', tracking=True)
    procedure_type = fields.Selection([
        ('emergency', 'Emergency'),
        ('non_emergency', 'Non-Emergency'),
        ('other', 'Other')
    ], string='Type Of Procedure', tracking=True)
    other_procedure_type = fields.Char('Other Type Of Procedure', tracking=True)
    graduation_to = fields.Selection([
        ('home', 'Home'),
        ('acceptance', 'Acceptance'),
        ('Referral', 'referral')
    ], string='Graduation To', tracking=True)
    doctor_id = fields.Many2one('hr.employee', string='Doctor', tracking=True)
    medication_request_ids = fields.One2many('em.hms.medication.request', 'gynochological_visit_id', string='Medication Requests')
    analysis_request_line_ids = fields.One2many('em.hms.analysis.request.line', 'gynochological_visit_id', string='Analysis Requests')
    image_request_line_ids = fields.One2many('em.hms.image.request.line', 'gynochological_visit_id', string='Image Requests')
    company_id = fields.Many2one('res.company', 'Medical Center', default = lambda self: self.env.company, required=True)
    notes = fields.Char('Notes', tracking=True)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
    ], string='Status', required=True, default='draft')
    
    _sql_constraints = [
        (
            'check_visit_datetime',
            'CHECK (visit_datetime <= NOW())',
            'Visit Date/Time Must Not Be Newer Than Now.'
        ),
    ]

    def confirm_record(self):
        self.ensure_one()
        self.medication_request_ids.generate_sale_order()
        self.env['em.hms.analysis.request'].generate_order(self, self.analysis_request_line_ids)
        self.env['em.hms.image.request'].generate_order(self, self.image_request_line_ids)
        self.write({
            'state': 'done'
        })