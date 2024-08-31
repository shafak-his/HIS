from odoo import _, api, fields, models, exceptions, tools


class EmHmsDialUrology(models.Model):
    _name = 'em.hms.dial.urology'
    _description = 'Urology Clinic'
    _rec_name = 'patient_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    patient_id = fields.Many2one('res.partner', 'Patient Name', required=True, domain=[('is_patient','=',True)])
    visit_datetime = fields.Datetime('Visit Date/Time', required=True, tracking=True)
    weight = fields.Float('Weight', tracking=True)
    medical_history = fields.Char('Medical History', tracking=True)
    diagnosis_id = fields.Many2one('em.hms.icd10', string='Diagnosis', required=True, tracking=True)
    stone_location = fields.Selection([
        ('kidney', 'Kidney'),
        ('ureter', 'Ureter'),
        ('bladder', 'Bladder')
    ], string='Stone Location', tracking=True)

    treatment = fields.Selection([
        ('referral_lithotripsy_department', 'Referral to lithotripsy department'),
        ('pharmaceutical', 'Pharmaceutical'),
        ('referral_another_hospital', 'Referral to another hospital')
    ], string='Treatment', required=True, tracking=True)

    notes = fields.Char('Notes', tracking=True)
    doctor_id = fields.Many2one('hr.employee', string='Doctor', tracking=True)
    medication_request_ids = fields.Many2many('product.template', 'dial_urology_product_medication_rel','clinic_visit_id', 'product_id', string='Medication Requests',domain="[('is_medication', '=', True)]")
    analysis_request_ids = fields.Many2many('product.template', 'dial_urology_product_analysis_rel','clinic_visit_id', 'product_id', string='Analysis Requests',domain="[('is_medical_analysis', '=', True)]")
    image_request_ids = fields.Many2many('product.template', 'dial_urology_product_image_rel', 'clinic_visit_id','product_id', string='Image Requests',domain="[('is_medical_imaging', '=', True)]")
    company_id = fields.Many2one('res.company', 'Medical Center', default = lambda self: self.env.company)
