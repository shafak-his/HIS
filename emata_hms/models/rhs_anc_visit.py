from odoo import _, api, fields, models, exceptions, tools


class EmHmsRHSANCVisit(models.Model):
    _name = 'em.hms.rhs.anc.visit'
    _description = 'ANC Visit'
    _rec_name = 'anc_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    anc_id = fields.Many2one('em.hms.rhs.anc', string='ANC', required=True)
    patient_id = fields.Many2one('res.partner', 'Patient Name', related='anc_id.patient_id')
    visit_date = fields.Date('Date Of Visit', required=True, tracking=True)
    is_signs = fields.Boolean('Signs (Pallor - Jaundice - Exophthalmos - Edema)', tracking=True)
    arterial_pressure = fields.Float('Arterial Pressure In Sitting Position', tracking=True)
    weight = fields.Float('Weight', tracking=True)
    fetal_hr = fields.Float('Fetal Heart Rate (n/d)', tracking=True)
    main_complaint = fields.Char('Main Complaint During This Visit', tracking=True)
    head_diameter = fields.Float('Measurement Of Head Diameter', tracking=True)
    thigh_length = fields.Float('Thigh Length', tracking=True)
    presence = fields.Selection([
        ('vertical', 'Vertical'),
        ('horizontal', 'Horizontal'),
        ('diagonal', 'Diagonal')
    ], string='Presence', tracking=True)
    fluid = fields.Selection([
        ('good', 'Good'),
        ('fluid_scarcity', 'Liquid Scarcity'),
        ('no_fluid', 'No Fluid'),
        ('amniotic_hydrocephalus', 'Amniotic Hydrocephalus')
    ], string='Fluid', tracking=True)
    deformities = fields.Char('Deformities', tracking=True)
    genital_age_in_weeks = fields.Integer('Genital Age In Weeks', tracking=True)
    vaginal_examination = fields.Selection([
        ('changed', 'Changed'),
        ('not_changed', 'Not Changed')
    ], string='Vaginal Examination If Performed', tracking=True)
    treatment = fields.Char('Treatment', tracking=True)
    is_tetanus_vaccined = fields.Boolean('Has The Patient Received The Tetanus Vaccine?', tracking=True)
    next_visit_date = fields.Date('Date Of Next Visit', tracking=True)
    examiner_name = fields.Char('Name Of Examiner', tracking=True)
    additional_notes = fields.Char('Additional Notes', tracking=True)
    analysis_request_ids = fields.Many2many('product.template', 'rhs_anc_visit_product_analysis_rel', 'anc_visit_id', 'product_id', string='Analysis Requests')
    company_id = fields.Many2one('res.company', 'Medical Center', default = lambda self: self.env.company)