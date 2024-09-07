from odoo import _, api, fields, models, exceptions, tools

class EmHmsNutritionMTMSG(models.Model):
    _name = 'em.hms.nutrition.mtmsg'
    _description = 'MTMSG'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    def _get_mtm_no(self):
        existing_records = self.search([('name', '!=', '1')])
        if existing_records:
            max_value = max(existing_records.mapped('name'), default=0)
            max_iter = int(str(max_value).replace('MTMs-', ''))
            return_value = f"MTMs-{(max_iter+1):03d}"
            return return_value
        else:
            return 'MTMs-001'
        
    name = fields.Char('Group Session NO', required=True, default=_get_mtm_no, tracking=True)
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
    number_pregnants_qt_eq_18 = fields.Integer('Number Of Pregnant women Over Or Equal To 18 Years', required=True, tracking=True)
    number_pregnants_lt_18 = fields.Integer('Number Of Pregnant women Under 18 Years', required=True, tracking=True)
    number_breastfeeding_qt_eq_18 = fields.Integer('Number Of Breastfeeding women Over Or Equal To 18 Years', required=True, tracking=True)
    number_breastfeeding_lt_18 = fields.Integer('Number Of Breastfeeding women Under 18 Years', required=True, tracking=True)
    number_female_caregivers_qt_eq_18 = fields.Integer('Number Of Female Caregivers Over Or Equal To 18 Years', required=True, tracking=True)
    number_female_caregivers_lt_18 = fields.Integer('Number Of Female Caregivers Under 18 Years', required=True, tracking=True)
    
    session_topic_ids = fields.Many2many('em.hms.nutrition.topic', 'mtmsg_topic_rel', 'mtmsg_id', 'session_topic_id', string='Session Topics', required=True, domain="[('category', '=', 'general')]")
    session_topic_iyc_ids = fields.Many2many('em.hms.nutrition.topic', 'mtmsg_topic_iyc_rel', 'mtmsg_id', 'session_topic_iyc_id', string='IYC Topics', domain="[('category', '=', 'iyc')]")
    other_iyc_topic = fields.Char('Other IYC Topic', tracking=True)
    session_topic_cholera_ids = fields.Many2many('em.hms.nutrition.topic', 'mtmsg_topic_cholera_rel', 'mtmsg_id', 'session_topic_cholera_id', string='Cholera Topics', domain="[('category', '=', 'cholera')]")
    other_cholera_topic = fields.Char('Other Corona Topic', tracking=True)
    session_topic_corona_ids = fields.Many2many('em.hms.nutrition.topic', 'mtmsg_topic_corona_rel', 'mtmsg_id', 'session_topic_corona_id', string='Corona Topics', domain="[('category', '=', 'corona')]")
    other_corona_topic = fields.Char('Other Corona Topic', tracking=True)
    session_topic_wash_ids = fields.Many2many('em.hms.nutrition.topic', 'mtmsg_topic_wash_rel', 'mtmsg_id', 'session_topic_wash_id', string='WASH Topics', domain="[('category', '=', 'wash')]")
    other_wash_topic = fields.Char('Other WASH Topic', tracking=True)
    session_topic_chronic_ids = fields.Many2many('em.hms.nutrition.topic', 'mtmsg_topic_chronic_rel', 'mtmsg_id', 'session_topic_chronic_id', string='Chronic Diseases Topics', domain="[('category', '=', 'chronic_diseases')]")
    other_chronic_topic = fields.Char('Other Chronic Diseases Topic', tracking=True)
    session_topic_infectious_ids = fields.Many2many('em.hms.nutrition.topic', 'mtmsg_topic_infectious_rel', 'mtmsg_id', 'session_topic_infectious_id', string='Infectious Diseases Topics', domain="[('category', '=', 'infectious_diseases')]")
    other_infectious_topic = fields.Char('Other Infectious Diseases Topic', tracking=True)
    session_topic_rh_ids = fields.Many2many('em.hms.nutrition.topic', 'mtmsg_topic_rh_rel', 'mtmsg_id', 'session_topic_rh_id', string='Reproductive Health Topics', domain="[('category', '=', 'rh')]")
    other_rh_topic = fields.Char('Other Reproductive Health Topic', tracking=True)
    
    is_iyc_topic = fields.Boolean(compute='_compute_is_iyc_topic', string='Is IYC Topic')
    is_iyc_topic_other = fields.Boolean(compute='_compute_is_iyc_topic', string='Other IYC Topic')
    is_cholera_topic = fields.Boolean(compute='_compute_is_cholera_topic', string='Is Cholera Topic')
    is_cholera_topic_other = fields.Boolean(compute='_compute_is_cholera_topic', string='Other Cholera Topic')
    is_corona_topic = fields.Boolean(compute='_compute_is_corona_topic', string='Is Corona Topic')
    is_corona_topic_other = fields.Boolean(compute='_compute_is_corona_topic', string='Other Corona Topic')
    is_wash_topic = fields.Boolean(compute='_compute_is_wash_topic', string='Is WASH Topic')
    is_wash_topic_other = fields.Boolean(compute='_compute_is_wash_topic', string='Other WASH Topic')
    is_chronic_topic = fields.Boolean(compute='_compute_is_chronic_topic', string='Is Chonic Diseases Topic')
    is_chronic_topic_other = fields.Boolean(compute='_compute_is_chronic_topic', string='Other Chonic Diseases Topic')
    is_infectious_topic = fields.Boolean(compute='_compute_is_infectious_topic', string='Is Infectious Diseases Topic')
    is_infectious_topic_other = fields.Boolean(compute='_compute_is_infectious_topic', string='Other Infectious Diseases Topic')
    is_rh_topic = fields.Boolean(compute='_compute_is_rh_topic', string='Is Reproductive Health Topic')
    is_rh_topic_other = fields.Boolean(compute='_compute_is_rh_topic', string='Other Reproductive Health Topic')
    
    @api.depends('session_topic_ids', 'session_topic_iyc_ids')
    def _compute_is_iyc_topic(self):
        for record in self:
            record.is_iyc_topic = 'iyc' in record.session_topic_ids.mapped('category') if record.session_topic_ids else False
            record.is_iyc_topic_other = 'iyc' in record.session_topic_ids.mapped('category') and 'Other' in record.session_topic_iyc_ids.mapped('name') if record.session_topic_ids and record.session_topic_iyc_ids else False
            
    @api.depends('session_topic_ids', 'session_topic_cholera_ids')
    def _compute_is_cholera_topic(self):
        for record in self:
            record.is_cholera_topic = 'cholera' in record.session_topic_ids.mapped('category') if record.session_topic_ids else False
            record.is_cholera_topic_other = 'cholera' in record.session_topic_ids.mapped('category') and 'Other' in record.session_topic_cholera_ids.mapped('name') if record.session_topic_ids and record.session_topic_cholera_ids else False
            
    @api.depends('session_topic_ids', 'session_topic_corona_ids')
    def _compute_is_corona_topic(self):
        for record in self:
            record.is_corona_topic = 'corona' in record.session_topic_ids.mapped('category') if record.session_topic_ids else False
            record.is_corona_topic_other = 'corona' in record.session_topic_ids.mapped('category') and 'Other' in record.session_topic_corona_ids.mapped('name') if record.session_topic_ids and record.session_topic_corona_ids else False
    
    @api.depends('session_topic_ids', 'session_topic_wash_ids')
    def _compute_is_wash_topic(self):
        for record in self:
            record.is_wash_topic = 'wash' in record.session_topic_ids.mapped('category') if record.session_topic_ids else False
            record.is_wash_topic_other = 'wash' in record.session_topic_ids.mapped('category') and 'Other' in record.session_topic_wash_ids.mapped('name') if record.session_topic_ids and record.session_topic_wash_ids else False
            
    @api.depends('session_topic_ids', 'session_topic_chronic_ids')
    def _compute_is_chronic_topic(self):
        for record in self:
            record.is_chronic_topic = 'chronic' in record.session_topic_ids.mapped('category') if record.session_topic_ids else False
            record.is_chronic_topic_other = 'chronic' in record.session_topic_ids.mapped('category') and 'Other' in record.session_topic_chronic_ids.mapped('name') if record.session_topic_ids and record.session_topic_chronic_ids else False
    
    @api.depends('session_topic_ids', 'session_topic_infectious_ids')
    def _compute_is_infectious_topic(self):
        for record in self:
            record.is_infectious_topic = 'infectious' in record.session_topic_ids.mapped('category') if record.session_topic_ids else False
            record.is_infectious_topic_other = 'infectious' in record.session_topic_ids.mapped('category') and 'Other' in record.session_topic_infectious_ids.mapped('name') if record.session_topic_ids and record.session_topic_infectious_ids else False
            
    @api.depends('session_topic_ids', 'session_topic_rh_ids')
    def _compute_is_rh_topic(self):
        for record in self:
            record.is_rh_topic = 'rh' in record.session_topic_ids.mapped('category') if record.session_topic_ids else False
            record.is_rh_topic_other = 'rh' in record.session_topic_ids.mapped('category') and 'Other' in record.session_topic_rh_ids.mapped('name') if record.session_topic_ids and record.session_topic_rh_ids else False
    
    number_mothers_educated_muac_qt_eq_18 = fields.Integer('Number Of Mothers Who Received Education On Their MUAC Measurement Greater Than Or Equal To 18', required=True, tracking=True)
    number_mothers_educated_muac_lt_18 = fields.Integer('Number Of Mothers Who Received Education On Their MUAC Measurement Under 18', required=True, tracking=True)
    
    company_id = fields.Many2one('res.company', 'Medical Center', default = lambda self: self.env.company)
    
    
    @api.onchange('location_id')
    def _onchange_location_id(self):
        if self.location_id and not self.sub_district_id:
            self.sub_district_id = self.location_id.sub_district_id.id
            self.district_id = self.location_id.sub_district_id.district_id.id
            self.state_id = self.location_id.sub_district_id.district_id.state_id.id
    
    
    
    