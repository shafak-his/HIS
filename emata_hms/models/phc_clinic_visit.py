from odoo import _, api, fields, models, exceptions, tools


class EmHmsPhcClinicVisit(models.Model):
    _name = 'em.hms.phc.clinic.visit'
    _description = 'PHC Clinic Visit'
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
    medical_history = fields.Char('Medical History', tracking=True)
    allergic_history = fields.Char('Allergic History', tracking=True)
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
    medication_request_ids = fields.Many2many('product.template', 'phc_clinic_visit_product_medication_rel', 'clinic_visit_id', 'product_id', string='Medication Requests', domain="[('is_medication', '=', True)]")
    analysis_request_ids = fields.Many2many('product.template', 'phc_clinic_visit_product_analysis_rel', 'clinic_visit_id', 'product_id', string='Analysis Requests', domain="[('is_medical_analysis', '=', True)]")
    image_request_ids = fields.Many2many('product.template', 'phc_clinic_visit_product_image_rel', 'clinic_visit_id', 'product_id', string='Image Requests', domain="[('is_medical_imaging', '=', True)]")
    company_id = fields.Many2one('res.company', 'Medical Center', default = lambda self: self.env.company, required=True)
    notes = fields.Char('Notes', tracking=True)
