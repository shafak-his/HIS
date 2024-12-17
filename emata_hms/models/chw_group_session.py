from odoo import _, api, fields, models, exceptions, tools


class EmHmsCHWGroupSession(models.Model):
    _name = 'em.hms.chw.group.session'
    _description = 'Group Session'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'em.base.common.form']
        
    name = fields.Char('Group Session No', tracking=True)
    service_place = fields.Selection([
        ('fixed', 'Fixed'),
        ('mobile', 'Mobile')
    ], string='Service Place', required=True, tracking=True)
    session_date = fields.Date('Session Date', required=True, tracking=True)
    center = fields.Selection([
        ('gene', 'Gene Center'),
        ('talada', 'Talada Center'),
        ('harbanoush', 'Harbanoush Center'),
        ('salqin', 'Salqin Center'),
        ('darkush', 'Darkush Center'),
        ('armanaz', 'Armanaz Center'),
        ('maarat_misrin', 'Maarat Misrin Center'),
        ('aryha', 'Aryha Center'),
        ('akhtarin', 'Akhtarin Center'),
        ('arshaf', 'Arshaf Center'),
        ('kfarghan', 'Kfarghan Center'),
        ('al_ziyadiah', 'Al-Ziyadiah Center'),
        ('al_ziyadiah_rh', 'Reproductive Health Center In Al-Ziyadiya')
    ], string='Center', required=True, tracking=True)
    community_health_worker_name  = fields.Char('Name Of Community Health Worker', required=True, tracking=True)
    session_title = fields.Selection([
        ('baby_care', 'BABY CARE'),
        ('breastfeeding', 'BREASTFEEDING'),
        ('child_marriage', 'CHILD MARRIAGE'),
        ('covid19', 'COVID 19'),
        ('drinking_water_treatment', 'DRINKNG WATER TREATMENT'),
        ('family_health', 'FAMILY HEALTH'),
        ('family_planning', 'FAMILY PALNNING'),
        ('home_envirinment', 'HOME ENVIRONMENT'),
        ('infectious_diseases', 'INFECTIOUS DISEASES'),
        ('personal_hygiene', 'PERSONAL HYGIENE'),
        ('other_diseases', 'OTHER DISEASES'),
        ('ncd_diseases', 'NCD DISEASES'),
        ('smoking', 'SMOKING'),
        ('pregnancy_care', 'PREGNANCY CARE'),
        ('proper_nutrition', 'PROPER NUTRITION'),
        ('pre_marriage_counseling', 'PRE-MARRIAGE COUNSELING')
    ], string='Session Title', required=True, tracking=True)
    target_group = fields.Selection([
        ('caregiver', 'CAREGIVER'),
        ('children', 'CHILDREN')
    ], string='Taregt Group', required=True, tracking=True)
    
    number_bnfs_gte_18 = fields.Integer('# Beneficiaries >= 18 Years', required=True, tracking=True)
    number_bnfs_lt_18 = fields.Integer('# Beneficiaries < 18 Years', required=True, tracking=True)
    bnf_ids = fields.One2many('em.hms.chw.group.session.bnf', 'session_id', string='Beneficiaries Information')
    
    company_id = fields.Many2one('res.company', 'Medical Center', default = lambda self: self.env.company)

    _sql_constraints = [
        (
            'check_session_date',
            'CHECK (session_date <= CURRENT_DATE)',
            'Session Date Must Not Be Newer Than Today.'
        ),
    ]
    
class EmHmsCHWGroupSessionBNF(models.Model):
    _name = 'em.hms.chw.group.session.bnf'
    _description = 'CHW Group Session Beneficiary'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    session_id = fields.Many2one('em.hms.chw.group.session', string='Session', ondelete='cascade')
    name = fields.Char('Beneficiary Name', required=True, tracking=True)
    name_lang = fields.Char('Arabic Name', required=True, tracking=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], string='Gender', required=True, tracking=True)
    bnf_status = fields.Selection([
        ('new', 'New'),
        ('old', 'Old')
    ], string='BNF Status', required=True, tracking=True)
    birth_date = fields.Date('Date Of Birth', required=True, tracking=True)
    displacement_status = fields.Selection([
        ('host', 'Host'),
        ('idp', 'IDP')
    ], string='Displacement Status', required=True, tracking=True)
    is_special_needs = fields.Binary('Does The Beneficiary Have Special Needs?', tracking=True)
    
    country_id = fields.Many2one('res.country', string='Country')
    state_id = fields.Many2one('res.country.state', string='Governorate', required=True, tracking=True)
    district_id = fields.Many2one('em.country.district', string='District', required=True, tracking=True)
    sub_district_id = fields.Many2one('em.country.sub.district', string='Sub-District', required=True, tracking=True)
    location_id = fields.Many2one('em.location', string='Village / City', required=True, tracking=True)
    is_location_camp = fields.Boolean('Is The Site A Camp?', tracking=True)
    camp_name = fields.Char('Camp Name', tracking=True)
    phone_number = fields.Char('Phone Number', tracking=True)
    comments = fields.Selection([
        ('sam_suffering', 'The Child Suffers From Severe Acute Malnutrition'),
        ('mam_suffering_child', 'The Child Suffers From Moderate Acute Malnutrition'),
        ('exclusive_breastfeeding', 'My Father Breastfeeds Exclusively'),
        ('mixed_breastfeeding', 'Mixed Breastfeeding'),
        ('breastfeeding_malnutrition', 'Malnutrition Of A Breastfeeding woman'),
        ('pregnant_malnutrition', 'Malnutrition Of A Pregnant Woman'),
        ('chronic_diseases', 'The Target Of The Session Suffers From A Chronic Disease')
    ], string='Comments', tracking=True)
    company_id = fields.Many2one('res.company', 'Medical Center', default = lambda self: self.env.company, required=True)    
    
    _sql_constraints = [
        (
            'check_birth_date',
            'CHECK (birth_date <= CURRENT_DATE)',
            'Birth Date Must Not Be Newer Than Today.'
        ),
    ]
    
    @api.onchange('sub_district_id')
    def _onchange_sub_district_update_location_domain(self):
        if self.sub_district_id:
            return {'domain': {'location_id': [('sub_district_id', '=', self.sub_district_id.id)]}}
        return {'domain': {'location_id': [(1, '=', 1)]}}

    @api.onchange('location_id')
    def _onchange_location_id(self):
        if self.location_id and not self.sub_district_id:
            self.sub_district_id = self.location_id.sub_district_id.id
            self.district_id = self.location_id.sub_district_id.district_id.id
            self.state_id = self.location_id.sub_district_id.district_id.state_id.id
            self.country_id = self.location_id.sub_district_id.district_id.state_id.country_id.id