from odoo import _, api, fields, models, exceptions, tools


class EmHmsCHWRHAwareness(models.Model):
    _name = 'em.hms.chw.rh.awareness'
    _description = 'RH Awareness'
    _rec_name = 'patient_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']
        
    patient_id = fields.Many2one('res.partner', 'Patient Name', required=True, domain=[('is_patient','=',True)])
    session_date = fields.Date('Session Date', required=True, tracking=True)
    community_health_worker_name  = fields.Char('Name Of Community Health Worker', required=True, tracking=True)
    project_id = fields.Many2one('project.project', string='Project Number', tracking=True)
    new_old = fields.Selection([
        ('new', 'New'),
        ('old', 'Old')
    ], string='New Or Old', required=True, tracking=True)
    
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
    comments = fields.Selection([
        ('sam_suffering', 'The Child Suffers From Severe Acute Malnutrition'),
        ('mam_suffering_child', 'The Child Suffers From Moderate Acute Malnutrition'),
        ('exclusive_breastfeeding', 'My Father Breastfeeds Exclusively'),
        ('mixed_breastfeeding', 'Mixed Breastfeeding'),
        ('breastfeeding_malnutrition', 'Malnutrition Of A Breastfeeding woman'),
        ('pregnant_malnutrition', 'Malnutrition Of A Pregnant Woman'),
        ('chronic_diseases', 'The Target Of The Session Suffers From A Chronic Disease')
    ], string='Comments', required=True, tracking=True)
    
    company_id = fields.Many2one('res.company', 'Medical Center', default = lambda self: self.env.company)
    

    _sql_constraints = [
        (
            'check_session_date',
            'CHECK (session_date <= CURRENT_DATE)',
            'Session Date Must Not Be Newer Than Today.'
        ),
    ]
    
    
    