from odoo import _, api, fields, models, exceptions, tools


class EmHmsMHGap(models.Model):
    _name = 'em.hms.mh.gap'
    _description = 'Mental Health Gap'
    _rec_name = 'session_date'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    session_date = fields.Date('Session Date', required=True, tracking=True)
    patient_id = fields.Many2one('res.partner', 'Patient Name', required=True, domain=[('is_patient','=',True)])
    educational_level = fields.Selection([
        ('primary_school', 'Primary School'),
        ('secondary', 'Secondary'),
        ('higher', 'Higher'),
        ('none', 'None')
    ], string='Educational Level', required=True, tracking=True)
    service_type = fields.Selection([
        ('mh', 'MH'),
        ('mhpss', 'MHPSS')
    ], string='Service Type', required=True, tracking=True)
    is_mh_assessment = fields.Boolean('Is Mental Health Assessment?', tracking=True)
    is_pss_service = fields.Boolean('Is PSS Service?', tracking=True)
    severity_score = fields.Selection([
        ('low', 'Low'),
        ('moderate', 'Moderate'),
        ('severe', 'Severe')
    ], string='Severity Score', required=True, tracking=True)
    principal_diagnosis = fields.Selection([
        ('depression', 'Depression'),
        ('bipolar_symptoms', 'Bipolar Symptoms'),
        ('asd_ptsd', 'Stress Related Symptoms (ASD, PTSD)'),
        ('oth', 'OTH'),
        ('epilepsy', 'Epilepsy'),
        ('behavioral_disorders', 'Behavioral Disorders'),
        ('learning_disability', 'Learning Disability (Mental Retardation)'),
        ('autistic', 'Autistic Spectrum Symptoms'),
        ('self_harm', 'Self Harm \ Suicide'),
        ('substance', 'Disorders Due To Substance Use')
    ], string='Principal Diagnosis According To The Gap Scale', required=True, tracking=True)
    file_status = fields.Selection([
        ('open', 'Open'),
        ('closed', 'Closed')
    ], string='What Is The Status Of The File', required=True, tracking=True)
    case_closure_date = fields.Date('Case Closure Date', required=True, tracking=True)
    pre_gaf = fields.Integer('Pre GAF', required=True, tracking=True)
    post_gaf = fields.Integer('Post GAF', required=True, tracking=True)
    closure_reason = fields.Selection([
        ('discharged', 'Discharged, All Goals Met'),
        ('tertiary_referral', 'Referral To Secondary/Tertiary Care'),
        ('medical_referral', 'Medical Referral'),
        ('agency_referral', 'Referred To Other Agency That Can Better Meet Needs'),
        ('moved', 'Moved To Other Area'),
        ('absent', 'Absent/Untraceable After 3 Contact Attempts'),
        ('wish_to_end', 'Wishes To End Follow-up'),
        ('other', 'Other Reason')
    ], string='Reasons For Closure', required=True, tracking=True)
    other_closure_reason = fields.Char('Other Reason For Closure', tracking=True)
    company_id = fields.Many2one('res.company', 'Medical Center', default = lambda self: self.env.company)
    service_provider_id = fields.Many2one('hr.employee', 'Service Provicer Name', required=True)
    medication_request_ids = fields.Many2many('product.template', 'mh_gap_product_medication_rel', 'mh_gap_id', 'product_id', string='Medication Requests', domain="[('is_medication', '=', True)]")
    
    