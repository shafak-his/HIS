from odoo import _, api, fields, models, exceptions, tools


class EmHmsMHReferral(models.Model):
    _name = 'em.hms.mh.referral'
    _description = 'Mental Health Referral'
    _rec_name = 'referral_date'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    referral_date = fields.Date('Referral Date', required=True, tracking=True)
    patient_id = fields.Many2one('res.partner', 'Patient Name', required=True, tracking=True)
    
    referral_path = fields.Selection([
        ('project_internal', 'Internal - Project Services'),
        ('org_external', 'External - Other Shafak Projects'),
        ('external', 'External - Other Service Providers')
    ], string='Referral Path', required=True, tracking=True)
    referred_via = fields.Selection([
        ('phone', 'Phone'),
        ('self_referral', 'Self Referral'),
        ('email', 'E-mail'),
        ('skype', 'Skype')
    ], string='Referred Via', required=True, tracking=True)
    severity = fields.Selection([
        ('high', 'High (Follow-up Within 24 Hours)'),
        ('moderate', 'Moderate (Follow-up Within 3 Days)'),
        ('low', 'Low (Follow-up Within 7 Days)')
    ], string='Severity', required=True, tracking=True)
    referral_code = fields.Char('Referral Code', required=True, tracking=True)
    privacy_confidentiality = fields.Selection([
        ('high', 'High'),
        ('moderate', 'Moderate'),
        ('low', 'Low')
    ], string='Privacy And Confidentiality Required For This Referral', required=True, tracking=True)
    key_protection_risks = fields.Selection([
        ('gbv', 'Gender Based Violation (GBV)'),
        ('sgbv', 'Sexual Gender Based Violation (SGBV)'),
        ('gp', 'General Protection (GP)'),
        ('cp', 'Child Protection (CP)')
    ], string='Key Protection Risks', required=True, tracking=True)
    referred_by_entity = fields.Char('Referred By (Entity)', required=True, tracking=True)
    referred_by_address = fields.Char('Referred By (Address)', tracking=True)
    referred_by_telephone = fields.Char('Referred By (Telephone)', tracking=True)
    referred_by_email = fields.Char('Referred By (E-mail)', tracking=True)
    referred_to_entity = fields.Char('Referred To (Entity)', required=True, tracking=True)
    referred_to_address = fields.Char('Referred To (Address)', tracking=True)
    referred_to_telephone = fields.Char('Referred To (Telephone)', tracking=True)
    referred_to_email = fields.Char('Referred To (E-mail)', tracking=True)
    services_required = fields.Selection([
        ('protection', 'Protection'),
        ('mecical', 'Mecical'),
        ('mental_health', 'Mental Health'),
        ('psychological_Support', 'Psychosocial Support'),
        ('legal_advice', 'Legal Advice'),
        ('livelihoods', 'Livelihoods'),
        ('shelter', 'Shelter'),
        ('nfi', 'NFI'),
        ('food_security', 'Food Security'),
        ('nutrition', 'Nutrition'),
        ('cva', 'CVA'),
        ('other', 'Other (Please Specify)')
    ], string='Services Required', required=True, tracking=True)
    where_to_submit_the_referral = fields.Char('Where To Submit The Referral', tracking=True)
    phone_privacy = fields.Selection([
        ('bnf_call', 'Beneficiary Will Call Referee'),
        ('bnf_visit', 'Beneficiary Will Visit Project Office'),
        ('allow_rp_call_service_provider', 'Allow Referee To Call Service Provider'),
        ('not_interested', 'Not Interested')
    ], string='Explain To The Beneficiary That The Phone Number Must Be Private And That Calling It Will Not Cause Any Harm To The Beneficiary Or Expose Privacy Or Breach Confidentiality', required=True, tracking=True)
    did_bnf_receive_referral_contact = fields.Boolean('The Beneficiary Has Been Provided With The Address And Contact Numbers Of The Referee?', tracking=True)
    did_bnf_receive_service_provider_contact = fields.Boolean('The Beneficiary Has Been Provided With The Address And Contact Numbers Of The Service Provider?', tracking=True)
    case_response = fields.Char('Response To The Case', tracking=True)
    service_providing_date = fields.Date('Service Providing Date', required=True, tracking=True)
    service_confirmed_by = fields.Selection([
        ('bnf', 'Beneficiary'),
        ('service_provider', 'Service Provider'),
        ('referee', 'Referee'),
        ('not_confirmed', 'Not Confirmed')
    ], string='Service Provision Confirmed By', required=True, tracking=True)
    not_confirmed_service_response = fields.Selection([
        ('high_privacy', 'High Privacy And Confidentiality'),
        ('bnf_not_interested', 'The Beneficiary Is Definitely Not Interested'),
        ('difficulty_communicating_sp', 'Difficulty Communicating With The Service Provider'),
        ('sp_not_cooperative', 'The Service Provider Is Not Cooperative'),
        ('interruption_bnf_referee', 'Interruption Of Communication Between The Beneficiary And The Referee'),
        ('not_yet', 'Not Yet'),
        ('other', 'Other (Please Specify)')
    ], string='Reason Of Not Confirming Service Provision', required=True, tracking=True)
    other_not_confirmed_service_response = fields.Char('Other Reason Of Not Confirming Service Provision', tracking=True)
    referee_id = fields.Many2one('hr.employee', string='Referee', required=True)
    referee_manager_id = fields.Many2one('hr.employee', string='Referee Line Manager', required=True)
    company_id = fields.Many2one('res.company', 'Medical Center', default = lambda self: self.env.company)