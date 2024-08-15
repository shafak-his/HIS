from odoo import _, api, fields, models, exceptions, tools


class EmHmsRHSANCVisit(models.Model):
    _name = 'em.hms.rhs.anc.visit'
    _description = 'ANC Visit'
    _rec_name = 'anc_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    anc_id = fields.Many2one('em.hms.rhs.anc', string='ANC', required=True)
    patient_id = fields.Many2one('res.partner', 'Patient Name', related='anc_id.patient_id')
    visit_date = fields.Date('Date Of Visit', required=True, tracking=True)
    is_signs = fields.Boolean('Signs (Pallor - Jaundice - Exophthalmos - Edema)', required=True, tracking=True)
    arterial_position = fields.Float('Arterial Pressure In Sitting Position', required=True, tracking=True)
    weight = fields.Float('Weight', required=True, tracking=True)
    fetal_hr = fields.Integer('Fetal Heart Rate (n/d)', required=True, tracking=True)
    main_complaint = fields.Char('Main Complaint During This Visit', tracking=True)
    head_diameter = fields.Float('Measurement Of Head Diameter', required=True, tracking=True)
    thigh_height = fields.Float('Thigh Height', required=True, tracking=True)
    presence = fields.Selection([
        ('vertical', 'Vertical'),
        ('horizontal', 'Horizontal'),
        ('diagonal', 'Diagonal')
    ], string='Presence', required=True, tracking=True)
    fluid = fields.Selection([
        ('good', 'vertical'),
        ('fluid_scarcity', 'Liquid Scarcity'),
        ('no_fluid', 'No Fluid'),
        ('amniotic_hydrocephalus', 'Amniotic Hydrocephalus')
    ], string='Fluid', required=True, tracking=True)
    deformities = fields.Char('Deformities', tracking=True)
    genital_age_in_weeks = fields.Integer('Genital Age In Weeks', required=True, tracking=True)
    vaginal_examination_if_performed = fields.Selection([
        ('changed', 'Changed'),
        ('not_changed', 'Not Changed')
    ], string='Vaginal Examination If Performed', required=True, tracking=True)
    treatment = fields.Char('Treatment', tracking=True)
    is_tetanus_vaccined = fields.Boolean('Has The Patient Received The Tetanus Vaccine?', required=True, tracking=True)
    next_visit_date = fields.Date('Date Of Next Visit', required=True, tracking=True)
    name_of_examiner = fields.Char('Name Of Examiner', required=True, tracking=True)
    additional_notes = fields.Char('Additional Notes', tracking=True)
    analysis_request_ids = fields.Many2many('product.template', 'rhs_anc_visit_product_analysis_rel', 'anc_visit_id', 'product_id', string='Analysis Requests')
    