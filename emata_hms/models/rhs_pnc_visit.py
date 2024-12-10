from odoo import _, api, fields, models, exceptions, tools


class EmHmsRHSPathologicalFind(models.Model):
    _name = 'em.hms.rhs.pathological.find'
    _description = 'Pathological Finding'
    _rec_name = 'name'

    name = fields.Char('Name', required=True)
    name_lang = fields.Char('Arabic Name', required=True)
    
    
class EmHmsRHSPostpartumComp(models.Model):
    _name = 'em.hms.rhs.postpartum.comp'
    _description = 'Postpartum Complication'
    _rec_name = 'name'

    name = fields.Char('Name', required=True)
    name_lang = fields.Char('Arabic Name', required=True)


class EmHmsRHSWound(models.Model):
    _name = 'em.hms.rhs.wound'
    _description = 'Wounds'
    _rec_name = 'name'

    name = fields.Char('Name', required=True)
    name_lang = fields.Char('Arabic Name', required=True)
    
    
class EmHmsRHSPNCVisit(models.Model):
    _name = 'em.hms.rhs.pnc.visit'
    _description = 'PNC Visit'
    _rec_name = 'pnc_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    pnc_id = fields.Many2one('em.hms.rhs.pnc', string='PNC', required=True)
    patient_id = fields.Many2one('res.partner', 'Patient Name', related='pnc_id.patient_id')
    visit_date = fields.Date('Date Of Visit', required=True, tracking=True)
    arterial_pressure = fields.Float('Arterial Pressure', tracking=True)
    temperature = fields.Float('Temperature', tracking=True)
    pulse = fields.Float('Pulse', tracking=True)
    breastfeeding = fields.Selection([
        ('exclusive_parenting', 'Exclusive Parenting'),
        ('non_exclusive_parenting', 'Non-Exclusive Parenting'),
        ('artificial_breastfeeding', 'Artificial Breastfeeding')
    ], string='Breastfeeding', tracking=True)
    is_tetanus_vaccined = fields.Boolean('Tetanus Vaccine', tracking=True)
    patient_complaint = fields.Char('Patient Complaint If Any', tracking=True)
    echo_findings = fields.Char('Echo Findings', tracking=True)
    examiner_name = fields.Char('Name Of Examiner', tracking=True)
    
    pathological_finding_ids = fields.Many2many('em.hms.rhs.pathological.find', 'rhs_pnc_visit_pathological_find_rel', 'pnc_visit_id', 'path_find_id', string='Pathological Findings',)
    postpartum_complication_ids = fields.Many2many('em.hms.rhs.postpartum.comp', 'rhs_pnc_visit_postpartum_comp_rel', 'pnc_visit_id', 'post_comp_id', string='Postpartum Complications')
    wound_ids = fields.Many2many('em.hms.rhs.wound', 'rhs_pnc_visit_wound_rel', 'pnc_visit_id', 'wound_id', string='Existing Wounds')
    
    medication_request_line_ids = fields.One2many('em.hms.medication.request.line', 'pnc_visit_id', string='Medication Requests')
    analysis_request_line_ids = fields.One2many('em.hms.analysis.request.line', 'pnc_visit_id', string='Analysis Requests')
    image_request_line_ids = fields.One2many('em.hms.image.request.line', 'pnc_visit_id', string='Image Requests')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
    ], string='Status', required=True, default='draft')

    company_id = fields.Many2one('res.company', 'Medical Center', default = lambda self: self.env.company)

    def confirm_record(self):
        self.ensure_one()
        self.medication_request_line_ids.generate_sale_order()
        self.env['em.hms.analysis.request'].generate_order(self, self.analysis_request_line_ids)
        self.env['em.hms.image.request'].generate_order(self, self.image_request_line_ids)
        self.write({
            'state': 'done'
        })