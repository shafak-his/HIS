from odoo import _, api, fields, models, exceptions, tools


class EmHmsRHSPathologicalFind(models.Model):
    _name = 'em.hms.rhs.pathological.find'
    _description = 'Pathological Finding'
    _rec_name = 'name'

    name = fields.Char('Name', required=True, translate=True)
    
    
class EmHmsRHSPostpartumComp(models.Model):
    _name = 'em.hms.rhs.postpartum.comp'
    _description = 'Postpartum Complication'
    _rec_name = 'name'

    name = fields.Char('Name', required=True, translate=True)


class EmHmsRHSWound(models.Model):
    _name = 'em.hms.rhs.wound'
    _description = 'Wounds'
    _rec_name = 'name'

    name = fields.Char('Name', required=True, translate=True)
    
    
class EmHmsRHSPNCVisit(models.Model):
    _name = 'em.hms.rhs.pnc.visit'
    _description = 'PNC Visit'
    _rec_name = 'pnc_id'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'em.common.form']
    
    pnc_id = fields.Many2one('em.hms.rhs.pnc', string='PNC', required=True)
    patient_id = fields.Many2one('res.partner', 'Patient Name', related='pnc_id.patient_id')
    doctor_id = fields.Many2one('hr.employee', string='Doctor', tracking=True, required=True)
    visit_date = fields.Date('Date Of Visit', required=True, tracking=True)
    duration_since_birth = fields.Selection([
        ('less_49hour', 'Less Than 48 Hour'),
        ('from_2_to_42day', 'From 2 To 42 Day'),
       
    ], string='Duration Since Birth', tracking=True, required=True)
    pnc_visit_reason= fields.Selection([
        ('mastitis', 'Mastitis'),
        ('puerperal_fever', 'Puerperal fever'),
        ('puerperal_infection_after_C-section', 'Puerperal infection, after C-section'),
        ('puerperal_infection_after_vaginal_delivery', 'Puerperal infection,after vaginal delivery'),
        ('newborn_complications', 'Newborn Complications'),
        ('other_reason', 'Other Reasons')
       
    ], string='PNC visit Reason', tracking=True, required=True)
    arterial_pressure = fields.Float('Arterial Pressure', tracking=True)
    arterial_pressure_new = fields.Char('Arterial Pressure', tracking=True ,default='0/0')
    temperature = fields.Float('Temperature', tracking=True)
    pulse = fields.Float('Pulse', tracking=True)
    is_referral = fields.Boolean('Has There Been A Referral?', tracking=True)
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
    
    
    
    breastfeeding = fields.Selection([
        ('exclusive_parenting', 'Exclusive Parenting'),
        ('non_exclusive_parenting', 'Non-Exclusive Parenting'),
        ('artificial_breastfeeding', 'Artificial Breastfeeding')
    ], string='Breastfeeding', tracking=True, required=True)
    is_tetanus_vaccined = fields.Boolean('Tetanus Vaccine', tracking=True)
    patient_complaint = fields.Char('Patient Complaint If Any', tracking=True)
    echo_findings = fields.Char('Echo Findings', tracking=True)
    examiner_name = fields.Char('Name Of Examiner', tracking=True, required=True)
    pathological_finding_ids = fields.Many2many('em.hms.rhs.pathological.find', 'rhs_pnc_visit_pathological_find_rel', 'pnc_visit_id', 'path_find_id', string='Pathological Findings',required=True)
    postpartum_complication_ids = fields.Many2many('em.hms.rhs.postpartum.comp', 'rhs_pnc_visit_postpartum_comp_rel', 'pnc_visit_id', 'post_comp_id', string='Postpartum Complications',required=True)
    wound_ids = fields.Many2many('em.hms.rhs.wound', 'rhs_pnc_visit_wound_rel', 'pnc_visit_id', 'wound_id', string='Existing Wounds',required=True)
    
    medication_request_line_ids = fields.One2many('em.hms.medication.request.line', 'pnc_visit_id', string='Medication Requests')
    analysis_request_line_ids = fields.One2many('em.hms.analysis.request.line', 'pnc_visit_id', string='Analysis Requests')
    image_request_line_ids = fields.One2many('em.hms.image.request.line', 'pnc_visit_id', string='Image Requests')
    state_medication = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
    ], string='medication Status Request', required=True, default='draft')
    state_analysis = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
    ], string='analysis Status Request', required=True, default='draft')
    state_image = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
    ], string='image Status Request', required=True, default='draft')
    notes = fields.Char('Notes', tracking=True)
    company_id = fields.Many2one('res.company', 'Medical Center', default = lambda self: self.env.company)

    

    def confirm_record_medication(self):
        self.ensure_one()
        self.medication_request_line_ids.generate_sale_order()
        self.write({
            'state_medication': 'done'
        })
        
    def confirm_record_analysis(self):
        self.ensure_one()
        self.env['em.hms.analysis.request'].generate_order(self, self.analysis_request_line_ids)
        self.write({
            'state_analysis': 'done'
        })
    def confirm_record_image(self):
        self.ensure_one()
        self.env['em.hms.image.request'].generate_order(self, self.image_request_line_ids)
        self.write({
            'state_image': 'done'
        })