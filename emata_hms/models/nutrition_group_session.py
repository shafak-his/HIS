from odoo import _, api, fields, models, exceptions, tools


class EmHmsNutritionTeam(models.Model):
    _name = 'em.hms.nutrition.team'
    _description = 'Nutrition Team'
    _rec_name = 'code'

    code = fields.Char('Team Code', required=True)
    name = fields.Char('Name', required=True)
    name_lang = fields.Char('Arabic Name', required=True)

class EmHmsNutritionTopic(models.Model):
    _name = 'em.hms.nutrition.topic'
    _description = 'Group Session Topic'
    _rec_name = 'name'

    name = fields.Char('Name', required=True)
    name_lang = fields.Char('Arabic Name', required=True)
    parent_id = fields.Many2one('em.hms.nutrition.topic', string='Parent')
    child_ids = fields.One2many('em.hms.nutrition.topic', 'parent_id', string='Items')

class EmHmsNutritionBNFVisit(models.Model):
    _name = 'em.hms.nutrition.bnf.visit'
    _description = 'Nutrition Beneficiary Visit'
    _rec_name = 'name'
    
    name = fields.Char('Visit Code', required=True)


class EmHmsNutritionGroupSession(models.Model):
    _name = 'em.hms.nutrition.group.session'
    _description = 'Group Session'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']
        
    session_type = fields.Selection([
        ('general', 'General'),
        ('mtmsg', 'MTMSG'),
        ('ftfsg', 'FTFSG'),
    ], string='Session Type', required=True)
    name = fields.Char('Group Session No', tracking=True)
    project_id = fields.Many2one('project.project', string='Project Number', tracking=True)
    visit_date = fields.Date('Visit Date', required=True, tracking=True)
    session_presenter_name = fields.Char('Session Presenter Name', tracking=True)
    
    country_id = fields.Many2one('res.country', string='Country')
    state_id = fields.Many2one('res.country.state', string='Governorate', required=True, tracking=True)
    district_id = fields.Many2one('em.country.district', string='District', required=True, tracking=True)
    sub_district_id = fields.Many2one('em.country.sub.district', string='Sub-District', required=True, tracking=True)
    location_id = fields.Many2one('em.location', string='Village / City', required=True, tracking=True)
    camp_name = fields.Char('Camp Name', required=True, tracking=True)
    
    team_id = fields.Many2one('em.hms.nutrition.team', string='Team', required=True, tracking=True)
    service_place = fields.Selection([
        ('fixed', 'Fixed'),
        ('mobile', 'Mobile')
    ], string='Service Place', required=True, tracking=True)
    number_pregnants_gte_18 = fields.Integer('# Pregnant Women >= 18 Years', required=True, tracking=True)
    number_pregnants_lt_18 = fields.Integer('# Pregnant Women < 18 Years', required=True, tracking=True)
    number_breastfeeding_gte_18 = fields.Integer('# Breastfeeding Women >= 18 Years', required=True, tracking=True)
    number_breastfeeding_lt_18 = fields.Integer('# Breastfeeding Women < 18 Years', required=True, tracking=True)
    number_female_caregivers_gte_18 = fields.Integer('# Female Caregivers >= 18 Years', required=True, tracking=True)
    number_female_caregivers_lt_18 = fields.Integer('# Female Caregivers < 18 Years', required=True, tracking=True)
    number_male_caregivers_gte_18 = fields.Integer('# Male Caregivers >= 18 Years', tracking=True)
    number_male_caregivers_lt_18 = fields.Integer('# Male Caregivers < 18 Years', tracking=True)

    topic_ids = fields.One2many('em.hms.nutrition.group.session.topic', 'session_id', string='Topics')

    number_mothers_educated_muac_gte_18 = fields.Integer('# Mothers MUAC Educated >= 18', required=True, tracking=True)
    number_mothers_educated_muac_lt_18 = fields.Integer('# Mothers MUAC Educated On Their MUAC Measurement < 18', required=True, tracking=True)

    bnf_ids = fields.One2many('em.hms.nutrition.group.session.bnf', 'session_id', string='Beneficiaries')
    
    company_id = fields.Many2one('res.company', 'Medical Center', default = lambda self: self.env.company)
    
    _sql_constraints = [
        (
            'check_visit_date',
            'CHECK (visit_date <= CURRENT_DATE)',
            'Visit Date Must Not Be in Future.'
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
    
    @api.model
    def create(self, vals):
        session_type = vals['session_type']
        if session_type == 'general':
            sequence_code = 'em.hms.nutrition.group.session.code'
        elif session_type == 'mtmsg':
            sequence_code = 'em.hms.nutrition.mtmsg.session.code'
        elif session_type == 'ftfsg':
            sequence_code = 'em.hms.nutrition.ftfsg.session.code'
        else:
            raise exceptions.ValidationError('Unexpected Error! Contact technical support.')

        vals['name'] = self.sudo().env['ir.sequence'].next_by_code(sequence_code)
        return super(EmHmsNutritionGroupSession, self).create(vals)
    
class EmHmsNutritionGroupSessionTopic(models.Model):
    _name = 'em.hms.nutrition.group.session.topic'
    _description = 'Nutrition Group Session Topic'
    
    session_id = fields.Many2one('em.hms.nutrition.group.session', string='Session', ondelete='cascade')
    topic_id = fields.Many2one('em.hms.nutrition.topic', string='Main Topic', required=True)
    sub_topic_ids = fields.Many2many('em.hms.nutrition.topic', string='Sub-Topic', required=True)
    other_sub_topics = fields.Char('Other Sub-Topics')

class EmHmsNutritionGroupSessionBNF(models.Model):
    _name = 'em.hms.nutrition.group.session.bnf'
    _description = 'Nutrition Beneficiary'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    session_id = fields.Many2one('em.hms.nutrition.group.session', string='Session', ondelete='cascade')
    name = fields.Char('Beneficiary Name', required=True, tracking=True)
    name_lang = fields.Char('Arabic Name', required=True, tracking=True)
    age = fields.Integer('Beneficiary Age', tracking=True)
    
    visit_ids = fields.Many2many('em.hms.nutrition.bnf.visit', 'nutrition_bnf_visit_rel', 'bnf_id', 'visit_id', string='Beneficiary Visits')