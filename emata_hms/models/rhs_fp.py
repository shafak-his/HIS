from odoo import _, api, fields, models, exceptions, tools


class EmHmsRHSFPProblem(models.Model):
    _name = 'em.hms.rhs.fp.problem'
    _description = 'Method-Related Health Problem'
    _rec_name = 'name'

    name = fields.Char('Name', required=True, translate=True)

class EmHmsRHSFPPregnancyCheck(models.Model):
    _name = 'em.hms.rhs.fp.pregnancy.check'
    _description = 'Check For Pregnancy'
    _rec_name = 'name'

    name = fields.Char('Name', required=True, translate=True)
    
class EmHmsRHSFPMedicalHistory(models.Model):
    _name = 'em.hms.rhs.fp.medical.history'
    _description = 'Medical History And Habit'
    _rec_name = 'name'

    name = fields.Char('Name', required=True, translate=True)

class EmHmsRHSFPComplaint(models.Model):
    _name = 'em.hms.rhs.fp.complaint'
    _description = 'Complaint'
    _rec_name = 'name'

    name = fields.Char('Name', required=True, translate=True)

class EmHmsRHSFPContraceptiveMethod(models.Model):
    _name = 'em.hms.rhs.fp.contraceptive.method'
    _description = 'Contraceptive Method'
    _rec_name = 'name'

    name = fields.Char('Name', required=True, translate=True)
    
class EmHmsRHSFP(models.Model):
    _name = 'em.hms.rhs.fp'
    _description = 'FP'
    _rec_name = 'patient_id'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'em.common.form']
    
    patient_id = fields.Many2one('res.partner', 'Patient Name', required=True, domain=[('is_patient','=',True)])
    husband_name = fields.Char('Husband\'s Name', tracking=True)
    visit_date = fields.Date('Date Of Visit', required=True, tracking=True)
    pregnancies_count = fields.Integer('# Pregnancies', tracking=True)
    births = fields.Integer('# Births', tracking=True)
    miscarriages_count = fields.Integer('# Miscarriages', tracking=True)
    live_births = fields.Integer('Live Births', tracking=True)
    last_birth_date = fields.Date('Last Birth Date', tracking=True, required=True)
    is_last_birth_alive = fields.Boolean('Is Last Birth Alive', tracking=True)
    breastfeeding_method = fields.Selection([
        ('normal', 'Normal'),
        ('artificial', 'Artificial'),
        ('mixed', 'Mixed')
    ], string='Breastfeeding Method', tracking=True, required=True)
    last_menstrual_date = fields.Date('First Day Of Last Menstrual Period', tracking=True, required=True)
    is_contraceptive_method = fields.Boolean('Any Previous Contraceptive Method', tracking=True)
    contraceptive_method_ids = fields.Many2many('em.hms.rhs.fp.contraceptive.method', 'fp_contraceptive_method_rel', 'fp_id', 'contraceptive_method_id', string='Contraceptive Method', tracking=True)
    contraceptive_method = fields.Selection([
        ('t1', 'بروجسترون أحادي الطور - مستخدم قديم'),
        ('t2', 'بروجسترون أحادي الطور - مستخدم لأول مرة'),
        ('t3', 'حبوب مركبة - مستخدم قديم'),
        ('t4', 'حبوب مركبة - مستخدم لأول مرة'),
        ('t5', 'استشارات حول منع الحمل'),
        ('t6', 'حبوب منع طارئة'),
        ('t7', 'غرسات - مستخدم قديم'),
        ('t8', 'غرسات - مستخدم لأول مرة'),
        ('t9', 'موانع الحمل عن طريق الحقن - مستخدم لأول مرة'),
        ('t10', 'لولب - مستخدم قديم'),
        ('t11', 'لولب - مستخدم لأول مرة'),
        ('t12', 'واقي - مستخدم قديم'),
        ('t13', 'واقي - مستخدم لأول مرة')
    ], string=' contraceptive Method', tracking=True)
    current_contraceptive_method = fields.Selection([
      ('t1', 'بروجسترون أحادي الطور - مستخدم قديم'),
        ('t2', 'بروجسترون أحادي الطور - مستخدم لأول مرة'),
        ('t3', 'حبوب مركبة - مستخدم قديم'),
        ('t4', 'حبوب مركبة - مستخدم لأول مرة'),
        ('t5', 'استشارات حول منع الحمل'),
        ('t6', 'حبوب منع طارئة'),
        ('t7', 'غرسات - مستخدم قديم'),
        ('t8', 'غرسات - مستخدم لأول مرة'),
        ('t9', 'موانع الحمل عن طريق الحقن - مستخدم لأول مرة'),
        ('t10', 'لولب - مستخدم قديم'),
        ('t11', 'لولب - مستخدم لأول مرة'),
        ('t12', 'واقي - مستخدم قديم'),
        ('t13', 'واقي - مستخدم لأول مرة')
    ], string=' Current contraceptive Method', tracking=True,required=True)
   


    is_method_staisfying = fields.Boolean('Satisfaction With Method', tracking=True)
    method_problem_ids = fields.Many2many('em.hms.rhs.fp.problem', 'fp_problem_rel', 'fp_id', 'problem_id', string='Method-Related Health Problems', tracking=True)
    usage_duration=fields.Char('Duration Of Use', tracking=True)
    is_method_stopped = fields.Boolean('Has Contraceptive Method Been Stopped?', tracking=True)
    stopping_date = fields.Date('When Was It Stopped?', tracking=True)
    stopping_reason = fields.Char('Stopping Reason', tracking=True)
    is_referral = fields.Boolean('Has There Been A Referral?', tracking=True)
    referral_center_reason = fields.Char('To Which Center Were You Referred And What Was The Reason?', tracking=True)
    pregnancy_check_ids = fields.Many2many('em.hms.rhs.fp.pregnancy.check', 'fp_pregnancy_check_rel', 'fp_id', 'pregnancy_check_id', string='Check For Current Pregnancy', tracking=True, required=True)
    medical_history_ids = fields.Many2many('em.hms.rhs.fp.medical.history', 'fp_medical_history_rel', 'fp_id', 'medical_history_id', string='Medical History And Habits', tracking=True)
    current_complaint_ids = fields.Many2many('em.hms.rhs.fp.complaint', 'fp_complaint_rel', 'fp_id', 'complaint_id', string='Any Current Complaint', tracking=True)
    medication_request_line_ids = fields.One2many('em.hms.medication.request.line', 'fp_visit_id', string='Medication Requests')
    analysis_request_line_ids = fields.One2many('em.hms.analysis.request.line', 'fp_visit_id', string='Analysis Requests')
    image_request_line_ids = fields.One2many('em.hms.image.request.line', 'fp_visit_id', string='Image Requests')
    recommendations = fields.Char('Recommendations And Treatment', tracking=True)
    examiner_id = fields.Many2one('hr.employee', string='Name Of Examiner', tracking=True, required=True)
    next_visit_date = fields.Date('Next Visit Date', tracking=True, required=True)
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
    
    _sql_constraints = [
        (
            'check_last_birth_date',
            'CHECK (last_birth_date <= CURRENT_DATE)',
            'Last Birth Date Must Not Be Newer Than Today.'
        ),
        (
            'check_last_menstrual_date',
            'CHECK (last_menstrual_date <= CURRENT_DATE)',
            'Last Menstrual Date Must Not Be Newer Than Today.'
        ),
        (
            'check_stopping_date',
            'CHECK (stopping_date <= CURRENT_DATE)',
            'Stopping Date Must Not Be Newer Than Today.'
        ),
        (
            'check_next_visit_date',
            'CHECK (next_visit_date >= CURRENT_DATE)',
            'Next Visit Date Must Not Be Older Than Today.'
        ),
    ]

    @api.onchange('patient_id')
    def _onchange_patient_id(self):
        if self.patient_id:
            self.medical_history_ids = [(6, 0, [record.id for record in self.patient_id.medical_history_ids])]
            
            
    
    