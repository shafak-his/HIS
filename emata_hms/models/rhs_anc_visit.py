from odoo import _, api, fields, models, exceptions, tools


class EmHmsRHSANCVisit(models.Model):
    _name = 'em.hms.rhs.anc.visit'
    _description = 'ANC Visit'
    _rec_name = 'anc_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    anc_id = fields.Many2one('em.hms.rhs.anc', string='ANC', required=True)
    patient_id = fields.Many2one('res.partner', 'Patient name', related='anc_id.patient_id')
    visit_date = fields.Date('Date of visit', required=True)
    is_signs = fields.Boolean('Signs (pallor-jaundice-exophthalmos-edema)', required=True, tracking=True)
    arterial_position = fields.Float('Arterial pressure in sitting position', required=True)
    weight = fields.Float('Weight', required=True)
    fetal_hr = fields.Integer('Fetal heart rate (n/d)', required=True)
    main_complaint = fields.Char('Main complaint during this visit')
    head_diameter = fields.Float('Measurement of head diameter', required=True)
    thigh_height = fields.Float('Thigh Height', required=True)
    presence = fields.Selection([
        ('vertical', 'Vertical'),
        ('horizontal', 'Horizontal'),
        ('diagonal', 'Diagonal')
    ], string='Presence', required=True, tracking=True)
    fluid = fields.Selection([
        ('good', 'vertical'),
        ('fluid_scarcity', 'Liquid Scarcity'),
        ('no_fluid', 'No Fluid'),
        ('amniotic_hydrocephalus', 'Amniotic hydrocephalus')
    ], string='Fluid', required=True, tracking=True)
    deformities = fields.Char('Deformities')
    genital_age_in_weeks = fields.Integer('Genital age in weeks', required=True)
    vaginal_examination_if_performed = fields.Selection([
        ('changed', 'Changed'),
        ('not_changed', 'Not Changed')
    ], string='Vaginal examination if performed', required=True, tracking=True)
    treatment = fields.Char('Treatment')
    is_tetanus_vaccined = fields.Boolean('Has the patient received the tetanus vaccine', required=True, tracking=True)
    next_visit_date = fields.Date('Date of next visit', required=True)
    name_of_examiner = fields.Char('Name of examiner', required=True)
    additional_notes = fields.Char('Additional notes')
    analysis_request_ids = fields.Many2many('product.template', 'rhs_anc_visit_product_rel', 'anc_visit_id', 'product_id', string='Request for analysis')
    