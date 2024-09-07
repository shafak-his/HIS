from odoo import _, api, fields, models, exceptions, tools

class EmHmsNutritionBNFVisit(models.Model):
    _name = 'em.hms.nutrition.bnf.visit'
    _description = 'Nutrition Beneficiary Visit'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char('Visit Code', required=True, tracking=True)
    
class EmHmsNutritionBNF(models.Model):
    _name = 'em.hms.nutrition.bnf'
    _description = 'Nutrition Beneficiary'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char('Beneficiary name', required=True, tracking=True)
    name_lang = fields.Char('Arabic name', required=True, tracking=True)
    age = fields.Integer('Age Of The Beneficiary', required=True, tracking=True)
    
    visit_ids = fields.Many2many('em.hms.nutrition.bnf.visit', 'nutrition_bnf_visit_rel', 'bnf_id', 'visit_id', string='Beneficiary Visits', required=True)
    
    
class EmHmsNutritionFTFSG(models.Model):
    _name = 'em.hms.nutrition.ftfsg'
    _description = 'FTFSG'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    def _get_ftf_no(self):
        existing_records = self.search([('name', '!=', '1')])
        if existing_records:
            max_value = max(existing_records.mapped('name'), default=0)
            max_iter = int(str(max_value).replace('FTFs-', ''))
            return_value = f"FTFs-{(max_iter+1):03d}"
            return return_value
        else:
            return 'FTFs-001'
        
    name = fields.Char('Group Session NO', required=True, default=_get_ftf_no, tracking=True)
    project_id = fields.Many2one('project.project', string='Project Number', tracking=True)
    visit_date = fields.Date('Date Of Visit', required=True, tracking=True)
    
    state_id = fields.Many2one('res.country.state', string='Governorate', required=True, tracking=True)
    district_id = fields.Many2one('em.country.district', string='District', required=True, tracking=True)
    sub_district_id = fields.Many2one('em.country.sub.district', string='Sub-District', required=True, tracking=True)
    location_id = fields.Many2one('em.location', string='Village / City', required=True, tracking=True)
    camp_name = fields.Char('Camp Name', required=True, tracking=True)
    
    team_code_id = fields.Many2one('em.hms.nutrition.team', string='Team Code', required=True, tracking=True)
    service_place = fields.Selection([
        ('fixed', 'Fixed'),
        ('mobile', 'Mobile')
    ], string='Place Where The Service Is Provided', required=True, tracking=True)
    session_presenter_name = fields.Char('Name Of The Session Presenter', required=True, tracking=True)
    number_male_caregivers_qt_eq_18 = fields.Integer('Number Of Male Caregivers Over Or Equal To 18 Years', tracking=True)
    number_male_caregivers_lt_18 = fields.Integer('Number Of Male Caregivers Under 18 Years', tracking=True)
    
    bnf_ids = fields.Many2many('em.hms.nutrition.bnf', 'nutrition_ftfsg_bnf_rel', 'ftfsg_id', 'bnf_id', string='Beneficiaries', required=True)
    
    company_id = fields.Many2one('res.company', 'Medical Center', default = lambda self: self.env.company)
    
    
    @api.onchange('location_id')
    def _onchange_location_id(self):
        if self.location_id and not self.sub_district_id:
            self.sub_district_id = self.location_id.sub_district_id.id
            self.district_id = self.location_id.sub_district_id.district_id.id
            self.state_id = self.location_id.sub_district_id.district_id.state_id.id
    
    
    
    