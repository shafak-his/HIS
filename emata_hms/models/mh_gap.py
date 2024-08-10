from odoo import _, api, fields, models, exceptions, tools


class EmHmsMHGAP(models.Model):
    _name = 'em.hms.mh.gap'
    _description = 'Mental Health GAP'
    _rec_name = 'session_date'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    session_date = fields.Date('Session Date', required=True)
    patient_id = fields.Many2one('res.partner', 'Patient name', required=True)
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
    is_mh_assessment = fields.Boolean('Mental Health Assessment', tracking=True)
    is_pss_service = fields.Boolean('PSS Service', tracking=True)
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
        ('learning_disability', 'Learning disability (Mental Retardation)'),
        ('autistic', 'Autistic Spectrum symptoms'),
        ('self_harm', 'Self Harm \ Suicide'),
        ('substance', 'Disorders due to substance use')
    ], string='Principal Diagnosis According to the Gap Scale', required=True, tracking=True)
    file_status = fields.Selection([
        ('open', 'Open'),
        ('closed', 'Closed')
    ], string='What is the Status of the File', required=True, tracking=True)
    case_closure_date = fields.Date('Case Closure Date', required=True)
    pre_gap = fields.Integer('Pre Gap', required=True)
    post_gap = fields.Integer('Post Gap', required=True)
    reasons_for_closure = fields.Selection([
        ('discharged', 'Discharged, all goals met'),
        ('tertiary_referral', 'Referral to secondary/tertiary care'),
        ('medical_referral', 'Medical Referral'),
        ('agency_referral', 'Referred to other agency that can better meet needs'),
        ('moved', 'Moved to other area'),
        ('absent', 'Absent/untraceable after 3 contact attempts'),
        ('wish_to_end', 'Wishes to end follow-up'),
        ('other', 'Other reason')
    ], string='Reasons For Closure', required=True, tracking=True)
    other_reason_for_closure = fields.Char('Other Reason For Closure')
    medical_center_id = fields.Many2one('res.company', 'Medical center', default = lambda self: self.env.company)
    service_provider_id=fields.Many2one('hr.employee', 'Service Provicer Name', required=True, tracking=True)
    medication_request_ids = fields.Many2many('product.template', 'phc_mh_gap_product_rel', 'mh_gap_id', 'product_id', string='Medication request')
    