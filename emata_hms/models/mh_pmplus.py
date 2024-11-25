from odoo import _, api, fields, models, exceptions, tools


class EmHmsMHPMPLUS(models.Model):
    _name = 'em.hms.mh.pmplus'
    _description = 'Mental Health PM+'
    _rec_name = 'session_date'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    session_date = fields.Date('Session Date', required=True, tracking=True)
    patient_id = fields.Many2one('res.partner', 'Patient Name', required=True, domain=[('is_patient','=',True)])
    mh_worker_id = fields.Many2one('hr.employee', string='Mental Health Worker Definition', required=True)
    educational_status = fields.Selection([
        ('primary_school', 'Primary School'),
        ('secondary', 'Secondary'),
        ('higher', 'Higher'),
        ('none', 'None')
    ], string='Educational Status', tracking=True)
    main_complaints = fields.Selection([
        ('depression', 'Depression'),
        ('anxiety', 'Anxiety'),
        ('psychological_stress', 'Psychological Stress'),
        ('loss_sadness', 'Loss And Sadness')
    ], string='Main Complaints Present', tracking=True)
    intervention = fields.Selection([
        ('pmplus', 'PM+ Service'),
        ('psychological_support', 'Psychological Support Services')
    ], string='Intervention', tracking=True)
    visit_type = fields.Selection([
        ('np', 'NP'),
        ('fu', 'Follow-up')
    ], string='Type Of Visit', tracking=True)
    referral_type = fields.Selection([
        ('internal', 'Internal'),
        ('external', 'External'),
        ('none', 'None')
    ], string='Type Of Referral', tracking=True)
    internal_referral = fields.Selection([
        ('gbv', 'GBV'),
        ('cp', 'CP'),
        ('health', 'Health'),
        ('nutrition', 'Nutrition'),
        ('education', 'Education'),
        ('food_security', 'Food Security'),
        ('water_hygiene', 'Water Hygiene'),
        ('other', 'Other')
    ], string='If Internal Referral, Specify', tracking=True)
    other_internal_referral = fields.Char('Specify Other Internal Referral', tracking=True)
    external_referral = fields.Selection([
        ('other_ngos', 'Other NGOs'),
        ('family', 'Family'),
        ('friend', 'Friend'),
        ('community_resources', 'Community Resources'),
        ('self_referral', 'Self Referral')
    ], string='If External Referral, Specify', tracking=True)
    referred_from_entity = fields.Char('Referred From Entity', tracking=True)
    referred_to_entity = fields.Char('Referred To Entity', tracking=True)
    risk_level = fields.Selection([
        ('low', 'Low'),
        ('moderate', 'Moderate'),
        ('severe', 'Severe')
    ], string='Risk Level', tracking=True)
    file_status = fields.Selection([
        ('open', 'Open'),
        ('closed', 'Closed')
    ], string='File Status', tracking=True)
    quest_centers_initial = fields.Integer('Health Questionnaire For Centers - Initial Test', tracking=True)
    quest_phq9_final = fields.Integer('PHQ9 Post-Test Final Test', tracking=True)
    case_closure_date = fields.Date('Case Closure Date', tracking=True)
    closure_reason = fields.Selection([
        ('discharged', 'Discharged, All Goals Met'),
        ('tertiary_referral', 'Referral To Secondary/Tertiary Care'),
        ('medical_referral', 'Medical Referral'),
        ('agency_referral', 'Referred To Other Agency That Can Better Meet Needs'),
        ('moved', 'Moved To Other Area'),
        ('absent', 'Absent/Untraceable After 3 Contact Attempts'),
        ('wish_to_end', 'Wishes To End Follow-up'),
        ('other', 'Other Reason')
    ], string='Reasons For Closure', tracking=True)
    other_closure_reason = fields.Char('Other Reason For Closure', tracking=True)
    company_id = fields.Many2one('res.company', 'Medical Center', default = lambda self: self.env.company)
    
    