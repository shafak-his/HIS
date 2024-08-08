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
    referred_via = fields.Selection([
        ('Telephone', 'telephone'),
        ('Self referral', 'self_referral'),
        ('E-mail', 'email'),
        ('Skype', 'skype')
    ], string='Referred Via', required=True, tracking=True)
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
        ('Gender Based Violation (GBV)', 'gbv'),
        ('Sexual Gender Based Violation (SGBV)', 'sgbv'),
        ('General Protection (GP)', 'gp'),
        ('Child Protection (CP)', 'cp')
    ], string='Privacy and Confidentiality Required for This Referral', required=True, tracking=True)
    referred_by_entity = fields.Char('Referred By (Entity)', required=True)
    referred_by_address = fields.Char('Referred By (Address)')
    referred_by_telephone = fields.Char('Referred By (Telephone)')
    referred_by_email = fields.Char('Referred By (E-mail)')
    referred_to_entity = fields.Char('Referred To (Entity)', required=True)
    referred_to_address = fields.Char('Referred To (Address)')
    referred_to_telephone = fields.Char('Referred To (Telephone)')
    referred_to_email = fields.Char('Referred To (E-mail)')
    services_required = fields.Selection([
        ('Protection', 'protection'),
        ('Mecical', 'mecical'),
        ('Mental health', 'mental_health'),
        ('Psychosocial support', 'psychological_Support'),
        ('Legal advice', 'legal_advice'),
        ('Livelihoods', 'livelihoods'),
        ('Shelter', 'shelter'),
        ('NFI', 'nfi'),
        ('Food Security', 'food_security'),
        ('Nutrition', 'nutrition'),
        ('CVA', 'cva'),
        ('Other (Please specify)', 'other')
    ], string='Services Required', required=True, tracking=True)
    where_to_submit_the_referral = fields.Char('Where To Submit The Referral')
    explain_that_telephone_number_is_private = fields.Selection([
        ('Beneficiary will call referral provider', 'bnf_call'),
        ('Beneficiary will visit project office', 'bnf_visit'),
        ('Allow referral provider to call referrerr', 'allow_rp_call_referrer')
    ], string='Explain to the beneficiary that the phone number must be private and that calling it will not cause any harm to the beneficiary or expose privacy or breach confidentiality')
    is_bnf_provided_referral_provider_address_contact = fields.Boolean('The beneficiary has been provided with the address and contact numbers of the referral provider')
    is_bnf_provided_referrer_address_contact = fields.Boolean('The beneficiary has been provided with the address and contact numbers of the referrer')
    response_to_the_case = fields.Char('Response To The Case')
    service_providing_date = fields.Date('Service Providing Date', required=True)
    service_provision_confirmed_by = fields.Selection([
        ('Beneficiary', 'bnf'),
        ('Referrer', 'referrer'),
        ('Referral Provider', 'referral_provider'),
        ('Not confirmed', 'not_confirmed')
    ], string='Service Provision Confirmed By')
    reason_of_not_confirming_service_provision = fields.Selection([
        ('High Privacy and Confidentiality', 'high_privacy_and_confidentiality'),
        ('The beneficiary is definitely not interested', 'bnf_not_interested'),
        ('Difficulty communicating with the service provider', 'difficulty_communicating_sp'),
        ('The service provider is not cooperative', 'sp_not_cooperative'),
        ('Interruption of communication between the beneficiary and the referral provider', 'interruption_bnf_referral_provider'),
        ('Not yet', 'not_yet'),
        ('Other (Please Specify)', 'other')
    ], string='Reason Of Not Confirming Service Provision')
    other_reason_of_not_confirming_service_provision = fields.Char('Other Reason Of Not Confirming Service Provision')
    referral_provider_id = fields.Many2one('hr.employee', string='Referral Provider')
    referral_provider_manager_id = fields.Many2one('hr.employee', string='Referral Provider Line Manager')