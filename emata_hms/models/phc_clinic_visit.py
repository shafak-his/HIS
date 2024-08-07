from odoo import _, api, fields, models, exceptions, tools


class EmHmsPhcClinicVisit(models.Model):
    _name = 'em.hms.phc.clinic.visit'
    _description = 'PHC Clinic Visit'
    _rec_name = 'visit_datetime'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    visit_datetime = fields.Datetime('Visit Date/Time', required=True)
    patient_id = fields.Many2one('res.partner', 'Patient name', required=True)
    clinic_id = fields.Many2one('em.hms.phc.clinic', string='Clinic name', required=True)
    is_pregnant = fields.Boolean('Is Pregnant?')
    is_lactating = fields.Boolean('Is Lactating?')
    temperature = fields.Float('Temperature', required=True)
    pulse = fields.Float('Pulse', required=True)
    pressure = fields.Char('Pressure', required=True)
    weight = fields.Float('Weight (KG)', required=True)
    height = fields.Float('Height (cm)', required=True)
    respiratory_rate=fields.Integer("Respiratory Rate",required=True)
    medical_history = fields.Char('Medical History')
    allergic_history = fields.Char('Allergic History')
    current_complaint = fields.Char('Current Complaint')
    diagnosis = fields.Many2one('em.hms.phc.icd10', required=True)
    diagnosis_code = fields.Char(string='Diagnosis Code', related='diagnosis_code.code')
    procedures_followed = fields.Char('Procedures Followed')
    type_of_procedure = fields.Selection([
        ('إسعافي', 'urgent'),
        ('بارد', 'cool'),
        ('آخر', 'other')
    ], string='Type Of Procedure', required=True, tracking=True)
    other_type_of_procedure = fields.Char('Other Type Of Procedure')
    doctor_id = fields.Many2one('hr.employee', string='Doctor', tracking=True)
    medication_request = fields.Many2many('product.template', string='Medication request')
    analysis_request = fields.Many2many('product.template', string='Analysis request')
    image_request = fields.Many2many('product.template', string='Image request')
    medical_center_id = fields.Many2one('res.company', 'Medical center', default = lambda self: self.env.company)
    notes = fields.Char('Notes')
