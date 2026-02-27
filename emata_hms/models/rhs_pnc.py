from odoo import _, api, fields, models, exceptions, tools
from odoo.exceptions import ValidationError

class EmHmsRHSPNC(models.Model):
    _name = 'em.hms.rhs.pnc'
    _description = 'PNC'
    _rec_name = 'patient_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    patient_id = fields.Many2one('res.partner', 'Patient Name', required=True, domain=[('is_patient','=',True)])
    husband_name = fields.Char('Husband\'s Name', tracking=True)
    
    birth_date = fields.Date('Date Of Birth', tracking=True, required=True)
    birth_type = fields.Selection([
        ('natural', 'Natural'),
        ('cesarean', 'Cesarean'),
        ('aided', 'Aided')
    ], string='Type Of Birth', tracking=True, required=True)
    is_baby_alive = fields.Boolean('Is The Baby Alive?', tracking=True)
    body_weight = fields.Float('Body Weight', tracking=True)
    is_full_term_pregnancy = fields.Boolean('Is Full Term Pregnancy (<37 weeks)?')
    birth_place = fields.Selection([
        ('home', 'Home'),
        ('medical_care_center', 'Medical Care Center'),
        ('hospital', 'Hospital')
    ], string='Place Of Birth', tracking=True, required=True)
    previous_complications = fields.Char('Previous Pregnancy And Birth Complications', tracking=True)
    is_referral = fields.Boolean('Has There Been A Referral?', tracking=True)
    referral_center_reason = fields.Char('To Which Center Were You Referred And What Was The Reason?', tracking=True)
    referral_type=fields.Selection([
        ('incoming_referrals_from_phc', 'احالة واردة من مركز عناية صحية أولية'),
        ('incoming_referrals_from_hospital', 'احالة واردة من مشفى اخر'),
        ('incoming_referrals_from_mobile_clinic', 'احالة واردة من عيادة جوالة'),
        ('referral_for_delivery_to_sdp_paid', 'احالة صادرة للولادة في مركز مدفوع'),
        ('referral_for_delivery_to_sdp_notpaid', 'احالة صادرة للولادة في مركز مجاني'),
        ('referral_to_GBV_advanced_services', 'احالة صادرة لخدمات GBV'),
        ('referral_to_advanced_services', 'احالة صادرة الى خدمات متقدمة'),
        ('referral_to_turkey', 'احالة الى تركيا')
       
    ], string='To Which Center Were You Referred And What Was The Reason?')
    visit_ids = fields.One2many('em.hms.rhs.pnc.visit', 'pnc_id', string='Periodic Visits')
    visits_count = fields.Integer(compute='_compute_visits_count', string='Visits Count')
    notes = fields.Char('Notes', tracking=True)
    company_id = fields.Many2one('res.company', 'Medical Center', default = lambda self: self.env.company)

    @api.depends('visit_ids')
    def _compute_visits_count(self):
        for record in self:
            record.visits_count=len(record.visit_ids)
            
    def action_get_pnc_visits_record(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'PNC Visits',
            'view_mode': 'tree',
            'res_model': 'em.hms.rhs.pnc.visit',
            'domain': [('pnc_id', '=', self.id)],
            'context': "{'create': False}"
        }
        
    @api.model
    def create(self, vals):
        # نتحقق من عدد السجلات المضافة في One2many
        visits = vals.get('visit_ids', [])
        count = len(visits)  # أوامر إضافة سجلات جديدة فقط
        
        if count <1:
            raise ValidationError("يجب إضافة زيارة واحدة على الاقل.")

        # نسمح لأودو بإنشاء السجل
        return super(EmHmsRHSPNC, self).create(vals)
    