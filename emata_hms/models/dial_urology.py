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
    diagnosis_id = fields.Many2one('em.hms.icd10', string='Diagnosis', tracking=True)
    stone_location = fields.Selection([
        ('kidney', 'Kidney'),
        ('ureter', 'Ureter'),
        ('bladder', 'Bladder')
    ], string='Stone Location', tracking=True)

    treatment = fields.Selection([
        ('referral_lithotripsy_department', 'Referral to lithotripsy department'),
        ('pharmaceutical', 'Pharmaceutical'),
        ('referral_another_hospital', 'Referral to another hospital')
    ], string='Treatment', tracking=True)

    notes = fields.Char('Notes', tracking=True)
    doctor_id = fields.Many2one('hr.employee', string='Doctor', tracking=True)

    medication_request_line_ids = fields.One2many('em.hms.medication.request.line', 'dial_urology_id', string='Medication Requests')
    analysis_request_line_ids = fields.One2many('em.hms.analysis.request.line', 'dial_urology_id', string='Analysis Requests')
    image_request_line_ids = fields.One2many('em.hms.image.request.line', 'dial_urology_id', string='Image Requests')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
    ], string='Status', required=True, default='draft')

    company_id = fields.Many2one('res.company', 'Medical Center', default = lambda self: self.env.company)

    def confirm_record(self):
        self.ensure_one()
        self.medication_request_line_ids.generate_sale_order()
        self.env['em.hms.analysis.request'].generate_order(self, self.analysis_request_line_ids)
        self.env['em.hms.image.request'].generate_order(self, self.image_request_line_ids)
        self.write({
            'state': 'done'
        })