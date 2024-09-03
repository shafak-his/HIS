from odoo import _, api, fields, models, exceptions, tools

class EmHmsNutritionTopic(models.Model):
    _name = 'em.hms.nutrition.topic'
    _description = 'Group Session Topic'
    _rec_name = 'name'

    name = fields.Char('Name', required=True)
    name_lang = fields.Char('Arabic Name', required=True)
    
class EmHmsNutritionTopicIYC(models.Model):
    _name = 'em.hms.nutrition.topic.iyc'
    _description = 'Group Session Topic - IYC'
    _rec_name = 'name'

    name = fields.Char('Name', required=True)
    name_lang = fields.Char('Arabic Name', required=True)

class EmHmsNutritionTopicCholera(models.Model):
    _name = 'em.hms.nutrition.topic.cholera'
    _description = 'Group Session Topic - Cholera'
    _rec_name = 'name'

    name = fields.Char('Name', required=True)
    name_lang = fields.Char('Arabic Name', required=True)
    
class EmHmsNutritionTopicCorona(models.Model):
    _name = 'em.hms.nutrition.topic.corona'
    _description = 'Group Session Topic - Corona'
    _rec_name = 'name'

    name = fields.Char('Name', required=True)
    name_lang = fields.Char('Arabic Name', required=True)

class EmHmsNutritionTopicWASH(models.Model):
    _name = 'em.hms.nutrition.topic.wash'
    _description = 'Group Session Topic - WASH'
    _rec_name = 'name'

    name = fields.Char('Name', required=True)
    name_lang = fields.Char('Arabic Name', required=True)
    
class EmHmsNutritionTopicChronic(models.Model):
    _name = 'em.hms.nutrition.topic.chronic'
    _description = 'Group Session Topic - Chronic Diseases'
    _rec_name = 'name'

    name = fields.Char('Name', required=True)
    name_lang = fields.Char('Arabic Name', required=True)
    
class EmHmsNutritionTopicInfectious(models.Model):
    _name = 'em.hms.nutrition.topic.infectious'
    _description = 'Group Session Topic - Infectious Diseases'
    _rec_name = 'name'

    name = fields.Char('Name', required=True)
    name_lang = fields.Char('Arabic Name', required=True)
    
class EmHmsNutritionTopicRH(models.Model):
    _name = 'em.hms.nutrition.topic.rh'
    _description = 'Group Session Topic - Reproductive Health RH'
    _rec_name = 'name'

    name = fields.Char('Name', required=True)
    name_lang = fields.Char('Arabic Name', required=True)
    
class EmHmsNutritionGroupSession(models.Model):
    _name = 'em.hms.nutrition.group.session'
    _description = 'Group Session'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char('Group Session NO', required=True, tracking=True)
    project_id = fields.Many2one('project.project', string='Project Number', required=True, tracking=True)
    visit_date = fields.Date('Date Of Visit', required=True, tracking=True)
    
    state_id = fields.Many2one('res.country.state', string='Governorate', required=True, tracking=True)
    district_id = fields.Many2one('em.country.district', string='District', required=True, tracking=True)
    sub_district_id = fields.Many2one('em.country.sub.district', string='Sub-District', required=True, tracking=True)
    location_id = fields.Many2one('em.location', string='Village / City', required=True, tracking=True)
    camp_name = fields.Char('Camp Name', required=True, tracking=True)
    
    service_place = fields.Selection([
        ('fixed', 'Fixed'),
        ('mobile', 'Mobile')
    ], string='Place Where The Service Is Provided', required=True, tracking=True)
    number_pregnants_qt_eq_18 = fields.Integer('Number Of Pregnant women Over Or Equal To 18 Years', required=True, tracking=True)
    number_pregnants_lt_18 = fields.Integer('Number Of Pregnant women Under 18 Years', required=True, tracking=True)
    number_breastfeeding_qt_eq_18 = fields.Integer('Number Of Breastfeeding women Over Or Equal To 18 Years', required=True, tracking=True)
    number_breastfeeding_lt_18 = fields.Integer('Number Of Breastfeeding women Under 18 Years', required=True, tracking=True)
    number_female_caregivers_qt_eq_18 = fields.Integer('Number Of Female Caregivers Over Or Equal To 18 Years', required=True, tracking=True)
    number_female_caregivers_lt_18 = fields.Integer('Number Of Female Caregivers Under 18 Years', required=True, tracking=True)
    number_male_caregivers_qt_eq_18 = fields.Integer('Number Of Male Caregivers Over Or Equal To 18 Years', tracking=True)
    number_male_caregivers_lt_18 = fields.Integer('Number Of Male Caregivers Under 18 Years', tracking=True)
    
    session_topic_ids = fields.Many2many('em.hms.nutrition.topic', 'nutrition_topic_rel', 'group_session_id', 'session_topic_id', string='Session Topic', required=True)
    session_topic_iyc_ids = fields.Many2many('em.hms.nutrition.topic.iyc', 'nutrition_topic_iyc_rel', 'group_session_id', 'session_topic_iyc_id', string='IYC Topics')
    other_iyc_topic = fields.Char('Other IYC Topic', tracking=True)
    session_topic_cholera_ids = fields.Many2many('em.hms.nutrition.topic.cholera', 'nutrition_topic_cholera_rel', 'group_session_id', 'session_topic_cholera_id', string='Cholera Topics')
    other_cholera_topic = fields.Char('Other Corona Topic', tracking=True)
    session_topic_corona_ids = fields.Many2many('em.hms.nutrition.topic.corona', 'nutrition_topic_corona_rel', 'group_session_id', 'session_topic_corona_id', string='Corona Topics')
    other_corona_topic = fields.Char('Other Corona Topic', tracking=True)
    session_topic_wash_ids = fields.Many2many('em.hms.nutrition.topic.wash', 'nutrition_topic_wash_rel', 'group_session_id', 'session_topic_wash_id', string='WASH Topics')
    other_wash_topic = fields.Char('Other WASH Topic', tracking=True)
    session_topic_chronic_ids = fields.Many2many('em.hms.nutrition.topic.chronic', 'nutrition_topic_chronic_rel', 'group_session_id', 'session_topic_chronic_id', string='Chronic Diseases Topics')
    other_chronic_topic = fields.Char('Other Chronic Diseases Topic', tracking=True)
    session_topic_infectious_ids = fields.Many2many('em.hms.nutrition.topic.infectious', 'nutrition_topic_infectious_rel', 'group_session_id', 'session_topic_infectious_id', string='Infectious Diseases Topics')
    other_infectious_topic = fields.Char('Other Infectious Diseases Topic', tracking=True)
    session_topic_rh_ids = fields.Many2many('em.hms.nutrition.topic.rh', 'nutrition_topic_rh_rel', 'group_session_id', 'session_topic_rh_id', string='Reproductive Health Topics')
    other_rh_topic = fields.Char('Other Reproductive Health Topic', tracking=True)
    is_iyc_topic = fields.Boolean(compute='_compute_is_iyc_topic', string='Is IYC Topic')
    is_cholera_topic = fields.Boolean(compute='_compute_is_cholera_topic', string='Is Cholera Topic')
    is_corona_topic = fields.Boolean(compute='_compute_is_corona_topic', string='Is Cholera Topic')
    is_wash_topic = fields.Boolean(compute='_compute_is_wash_topic', string='Is Cholera Topic')
    is_chronic_topic = fields.Boolean(compute='_compute_is_chronic_topic', string='Is Cholera Topic')
    is_infectious_topic = fields.Boolean(compute='_compute_is_infectious_topic', string='Is Cholera Topic')
    is_rh_topic = fields.Boolean(compute='_compute_is_rh_topic', string='Is Cholera Topic')
    
    @api.depends('session_topic_ids')
    def _compute_is_iyc_topic(self):
        for record in self:
            record.is_iyc_topic = 'IYC' in record.session_topic_ids.mapped('name')
            
    @api.depends('session_topic_ids')
    def _compute_is_cholera_topic(self):
        for record in self:
            record.is_cholera_topic = 'Cholera' in record.session_topic_ids.mapped('name')
            
    @api.depends('session_topic_ids')
    def _compute_is_corona_topic(self):
        for record in self:
            record.is_corona_topic = 'Corona' in record.session_topic_ids.mapped('name')
    
    @api.depends('session_topic_ids')
    def _compute_is_wash_topic(self):
        for record in self:
            record.is_wash_topic = 'WASH' in record.session_topic_ids.mapped('name')
            
    @api.depends('session_topic_ids')
    def _compute_is_chronic_topic(self):
        for record in self:
            record.is_chronic_topic = 'Chronic' in record.session_topic_ids.mapped('name')
    
    @api.depends('session_topic_ids')
    def _compute_is_infectious_topic(self):
        for record in self:
            record.is_infectious_topic = 'infectious' in record.session_topic_ids.mapped('name')
            
    @api.depends('session_topic_ids')
    def _compute_is_rh_topic(self):
        for record in self:
            record.is_rh_topic = 'Reproductive Health' in record.session_topic_ids.mapped('name')
    
    number_mothers_educated_muac_qt_eq_18 = fields.Integer('Number Of Mothers Who Received Education On Their MUAC Measurement Greater Than Or Equal To 18', required=True, tracking=True)
    number_mothers_educated_muac_lt_18 = fields.Integer('Number Of Mothers Who Received Education On Their MUAC Measurement Under 18', required=True, tracking=True)
    
    company_id = fields.Many2one('res.company', 'Medical Center', default = lambda self: self.env.company)
    
    
    # @api.onchange('location_id')
    # def _onchange_location_id(self):
    #     if self.location_id and not self.sub_district_id:
    #         self.sub_district_id = self.location_id.sub_district_id.id
    #         self.district_id = self.location_id.sub_district_id.district_id.id
    #         self.state_id = self.location_id.sub_district_id.district_id.state_id.id
    #         self.country_id = self.location_id.sub_district_id.district_id.state_id.country_id.id
    
    
    
    