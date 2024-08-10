from odoo import _, api, fields, models, exceptions, tools


class EmHmsMHReferral(models.Model):
    _name = 'em.hms.mh.referral'
    _description = 'Mental Health Referral'
    _rec_name = 'referral_date'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    referral_date = fields.Date('Referral Date', required=True)
    patient_id = fields.Many2one('res.partner', 'Patient name', required=True)
    
    referral_path = fields.Selection([
        ('project_internal', 'Internal - Project Services'),
        ('shafak_internal', 'External - Another Shafak Projects'),
        ('external', 'External - Another Services Providers')
    ], string='Referral Path', required=True, tracking=True)
    referred_via = fields.Selection([
        ('telephone', 'Telephone'),
        ('self_referral', 'Self referral'),
        ('email', 'E-mail'),
        ('skype', 'Skype')
    ], string='Referred Via', required=True, tracking=True)
    severity = fields.Selection([
        ('high', 'High (follow-up within 24 hours)'),
        ('moderate', 'Moderate (follow-up within 3 days)'),
        ('low', 'Low (follow-up within 7 days)')
    ], string='Severity', required=True, tracking=True)
    referral_code = fields.Char('Referral Code', required=True)
    privacy_confidentiality = fields.Selection([
        ('high', 'High'),
        ('moderate', 'Moderate'),
        ('low', 'Low')
    ], string='Privacy and Confidentiality Required for This Referral', required=True, tracking=True)
    key_protection_risks = fields.Selection([
        ('gbv', 'Gender Based Violation (GBV)'),
        ('sgbv', 'Sexual Gender Based Violation (SGBV)'),
        ('gp', 'General Protection (GP)'),
        ('cp', 'Child Protection (CP)')
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
        ('protection', 'Protection'),
        ('mecical', 'Mecical'),
        ('mental_health', 'Mental health'),
        ('psychological_Support', 'Psychosocial support'),
        ('legal_advice', 'Legal advice'),
        ('livelihoods', 'Livelihoods'),
        ('shelter', 'Shelter'),
        ('nfi', 'NFI'),
        ('food_security', 'Food Security'),
        ('nutrition', 'Nutrition'),
        ('cva', 'CVA'),
        ('other', 'Other (Please specify)')
    ], string='Services Required', required=True, tracking=True)
    where_to_submit_the_referral = fields.Char('Where To Submit The Referral')
    explain_that_telephone_number_is_private = fields.Selection([
        ('bnf_call', 'Beneficiary will call referral provider'),
        ('bnf_visit', 'Beneficiary will visit project office'),
        ('allow_rp_call_referrer', 'Allow referral provider to call referrerr')
    ], string='Explain to the beneficiary that the phone number must be private and that calling it will not cause any harm to the beneficiary or expose privacy or breach confidentiality', required=True)
    is_bnf_provided_referral_provider_address_contact = fields.Boolean('The beneficiary has been provided with the address and contact numbers of the referral provider')
    is_bnf_provided_referrer_address_contact = fields.Boolean('The beneficiary has been provided with the address and contact numbers of the referrer')
    response_to_the_case = fields.Char('Response To The Case')
    service_providing_date = fields.Date('Service Providing Date', required=True, tracking=True)
    service_provision_confirmed_by = fields.Selection([
        ('bnf', 'Beneficiary'),
        ('referrer', 'Referrer'),
        ('referral_provider', 'Referral Provider'),
        ('not_confirmed', 'Not confirmed')
    ], string='Service Provision Confirmed By', required=True, tracking=True)
    reason_of_not_confirming_service_provision = fields.Selection([
        ('high_privacy_and_confidentiality', 'High Privacy and Confidentiality'),
        ('bnf_not_interested', 'The beneficiary is definitely not interested'),
        ('difficulty_communicating_sp', 'Difficulty communicating with the service provider'),
        ('sp_not_cooperative', 'The service provider is not cooperative'),
        ('interruption_bnf_referral_provider', 'Interruption of communication between the beneficiary and the referral provider'),
        ('not_yet', 'Not yet'),
        ('other', 'Other (Please Specify)')
    ], string='Reason Of Not Confirming Service Provision', required=True, tracking=True)
    other_reason_of_not_confirming_service_provision = fields.Char('Other Reason Of Not Confirming Service Provision')
    referral_provider_id = fields.Many2one('hr.employee', string='Referral Provider')
    referral_provider_manager_id = fields.Many2one('hr.employee', string='Referral Provider Line Manager')