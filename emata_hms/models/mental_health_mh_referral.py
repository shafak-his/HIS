from odoo import _, api, fields, models, exceptions, tools


class EmHmsMentalHealthMHReferral(models.Model):
    _name = 'em.hms.mentalhealth.mh.referral'
    _description = 'PHC Clinic Visit'
    _rec_name = 'referral_date'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    referral_date = fields.Date('Referral Date', required=True)
    
    referral_path = fields.Selection([
        ('Internal - Project Services', 'project_internal'),
        ('External - Another Shafak Projects', 'shafak_internal'),
        ('External - Another Services Providers', 'external')
    ], string='Referral Path', required=True, tracking=True)
    referred_by = fields.Selection([
        ('Telephone', 'telephone'),
        ('Self referral', 'self_referral'),
        ('E-mail', 'email'),
        ('Skype', 'skype')
    ], string='Referred By', required=True, tracking=True)
    severity = fields.Selection([
        ('High (follow-up within 24 hours)', 'high'),
        ('Moderate (follow-up within 3 days)', 'moderate'),
        ('Low (follow-up within 7 days)', 'low')
    ], string='Severity', required=True, tracking=True)
    referral_code = fields.Char('Referral Code', required=True)
    privacy_confidentiality = fields.Selection([
        ('High', 'high'),
        ('Moderate', 'moderate'),
        ('Low', 'low')
    ], string='Privacy and Confidentiality Required for This Referral', required=True, tracking=True)
    key_protection_risks = fields.Selection([
        ('High', 'high'),
        ('Moderate', 'moderate'),
        ('Low', 'low')
    ], string='Privacy and Confidentiality Required for This Referral', required=True, tracking=True)
    