from odoo import _, api, fields, models, exceptions, tools


class EmHmsGeneralClinicVisit(models.Model):
    _name = 'em.hms.general.clinic.visit'
    _description = 'General Clinic Visit'
    _rec_name = 'visit_datetime'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    visit_datetime = fields.Datetime('Visit Date/Time', required=True, tracking=True)
    patient_id = fields.Many2one('res.partner', string='Patient Name', required=True, domain=[('is_patient','=',True)], tracking=True)
    clinic_id = fields.Many2one('em.hms.clinic', string='Clinic Name', tracking=True)
    is_pregnant = fields.Boolean('Is Pregnant?', tracking=True)
    is_lactating = fields.Boolean('Is Lactating?', tracking=True)
    temperature = fields.Float('Temperature', tracking=True)
    pulse = fields.Float('Pulse', tracking=True)
    pressure = fields.Float('Pressure', tracking=True)
    weight = fields.Float('Weight (KG)', tracking=True)
    height = fields.Float('Height (CM)', tracking=True)
    respiratory_rate = fields.Float('Respiratory Rate', tracking=True)
    medical_history_ids = fields.Many2many('em.hms.medical.history', 'general_clinic_visit_medical_history_rel', 'general_clinic_visit_id', 'medical_history_id', string='Medical History')
    allergic_history_ids = fields.Many2many('em.hms.allergic.history', 'general_clinic_visit_allergic_history_rel', 'general_clinic_visit_id', 'allergic_history_id', string='Allergic History')
    
    current_complaint = fields.Char('Current Complaint', tracking=True)
    diagnosis_id = fields.Many2one('em.hms.icd10', string='Diagnosis', tracking=True)
    procedures_followed = fields.Char('Procedures Followed', tracking=True)
    procedure_type = fields.Selection([
        ('emergency', 'Emergency'),
        ('non_emergency', 'Non-Emergency'),
        ('other', 'Other')
    ], string='Type Of Procedure', tracking=True)
    other_procedure_type = fields.Char('Other Type Of Procedure')
    doctor_id = fields.Many2one('hr.employee', string='Doctor', tracking=True)
    medication_request_line_ids = fields.One2many('em.hms.medication.request.line', 'general_visit_id', string='Medication Requests')
    analysis_request_line_ids = fields.One2many('em.hms.analysis.request.line', 'general_visit_id', string='Analysis Requests')
    image_request_line_ids = fields.One2many('em.hms.image.request.line', 'general_visit_id', string='Image Requests')
    company_id = fields.Many2one('res.company', 'Medical Center', default = lambda self: self.env.company, required=True)
    notes = fields.Char('Notes', tracking=True)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
    ], string='Status', required=True, default='draft')
    project_id = fields.Many2one('project.project', string='Project', tracking=True)
    allowed_project_ids = fields.Many2many('project.project', compute='_compute_allowed_project_ids', string='Allowed Projects', compute_sudo=True)

    @api.onchange('allowed_project_ids')
    def _onchange_allowed_project_ids(self):
        if self.allowed_project_ids:
            self.project_id = self.allowed_project_ids[0].id
        else:
            self.project_id = False

    @api.depends('company_id', 'clinic_id')
    def _compute_allowed_project_ids(self):
        for record in self:
            record.allowed_project_ids = self.env['em.project.support.line'].get_project_ids(record.company_id, self._name, self.clinic_id, fields.Date.today()).ids


    def confirm_record(self):
        self.ensure_one()
        self.medication_request_line_ids.generate_sale_order()
        self.env['em.hms.analysis.request'].generate_order(self, self.analysis_request_line_ids)
        self.env['em.hms.image.request'].generate_order(self, self.image_request_line_ids)
        self.write({
            'state': 'done'
        })