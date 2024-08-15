from odoo import _, api, fields, models, exceptions, tools


class EmHmsRHSPNCVisitPathFind(models.Model):
    _name = 'em.hms.rhs.pnc.visit.path.find'
    _description = 'Pathological Finding'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Name', required=True)
    name_lang = fields.Char('Arabic Name', required=True)
    
    
class EmHmsRHSPNCVisitPostComp(models.Model):
    _name = 'em.hms.rhs.pnc.visit.post.comp'
    _description = 'Postpartum Complication'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Name', required=True)
    name_lang = fields.Char('Arabic Name', required=True)


class EmHmsRHSPNCVisitExistWound(models.Model):
    _name = 'em.hms.rhs.pnc.visit.exist.wound'
    _description = 'Existing Wound'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

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
    arterial_pressure = fields.Float('Arterial Pressure', required=True, tracking=True)
    temperature = fields.Float('Temperature', required=True, tracking=True)
    pulse = fields.Integer('Pulse', required=True, tracking=True)
    breastfeeding = fields.Selection([
        ('exclusive_parenting', 'Exclusive Parenting'),
        ('non_exclusive_parenting', 'Non-Exclusive Parenting'),
        ('artificial_breastfeeding', 'Artificial Breastfeeding')
    ], string='Breastfeeding', required=True, tracking=True)
    is_tetanus_vaccined = fields.Boolean('Tetanus Vaccine', required=True, tracking=True)
    patient_complaint = fields.Char('Patient Complaint If Any', tracking=True)
    echo_findings = fields.Char('Echo Findings', tracking=True)
    name_of_examiner = fields.Char('Name Of Examiner', required=True, tracking=True)
    pathological_finding_ids = fields.Many2many('em.hms.rhs.pnc.visit.path.find', 'rhs_pnc_visit_path_find_rel', 'pnc_visit_id', 'path_find_id', string='Pathological Findings', required=True)
    postpartum_complication_ids = fields.Many2many('em.hms.rhs.pnc.visit.post.comp', 'rhs_pnc_visit_post_comp_rel', 'pnc_visit_id', 'post_comp_id', string='Postpartum Complications', required=True)
    existing_wound_ids = fields.Many2many('em.hms.rhs.pnc.visit.exist.wound', 'rhs_pnc_visit_exist_wound_rel', 'pnc_visit_id', 'exist_wound_id', string='Existing Wounds', required=True)
    
    medication_request_ids = fields.Many2many('product.template', 'rhs_pnc_visit_product_medication_rel', 'pnc_visit_id', 'product_id', string='Medication Requests', domain="[('is_medication', '=', True)]")
    analysis_request_ids = fields.Many2many('product.template', 'rhs_pnc_visit_product_analysis_rel', 'pnc_visit_id', 'product_id', string='Analysis Requests', domain="[('is_medical_analysis', '=', True)]")
    image_request_ids = fields.Many2many('product.template', 'rhs_pnc_visit_product_image_rel', 'pnc_visit_id', 'product_id', string='Image Requests', domain="[('is_medical_imaging', '=', True)]")
    
    