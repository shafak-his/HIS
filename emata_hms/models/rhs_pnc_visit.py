from odoo import _, api, fields, models, exceptions, tools


class EmHmsRHSPNCVisitPathFind(models.Model):
    _name = 'em.hms.rhs.pnc.visit.path.find'
    _description = 'PNC Visit Pathological findings'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Name', required=True)
    name_lang = fields.Char('Arabic Name', required=True)
    
    
class EmHmsRHSPNCVisitPostComp(models.Model):
    _name = 'em.hms.rhs.pnc.visit.post.comp'
    _description = 'PNC Visit Postpartum complications'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Name', required=True)
    name_lang = fields.Char('Arabic Name', required=True)


class EmHmsRHSPNCVisitExistWound(models.Model):
    _name = 'em.hms.rhs.pnc.visit.exist.wound'
    _description = 'PNC Visit Existing wounds'
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
    patient_id = fields.Many2one('res.partner', 'Patient name', related='pnc_id.patient_id')
    visit_date = fields.Date('Date of visit', required=True)
    arterial_pressure = fields.Float('Arterial pressure', required=True)
    temperature = fields.Float('Temperature', required=True)
    pulse = fields.Integer('Pulse', required=True)
    breastfeeding = fields.Selection([
        ('exclusive_parenting', 'Exclusive parenting'),
        ('non_exclusive_parenting', 'Non-Exclusive parenting'),
        ('artificial_breastfeeding', 'Artificial breastfeeding')
    ], string='Breastfeedingd', required=True, tracking=True)
    is_tetanus_vaccined = fields.Boolean('Tetanus vaccine', required=True, tracking=True)
    patient_complaint = fields.Char('Patient complaint if any')
    echo_findings = fields.Char('Echo findings')
    name_of_examiner = fields.Char('Name of examiner', required=True)
    pathological_finding_ids = fields.Many2many('em.hms.rhs.pnc.visit.path.find', 'rhs_pnc_visit_path_find_rel', 'pnc_visit_id', 'path_find_id', string='Pathological findings', required=True)
    postpartum_complication_ids = fields.Many2many('em.hms.rhs.pnc.visit.post.comp', 'rhs_pnc_visit_post_comp_rel', 'pnc_visit_id', 'post_comp_id', string='Postpartum complications', required=True)
    existing_wound_ids = fields.Many2many('em.hms.rhs.pnc.visit.exist.wound', 'rhs_pnc_visit_exist_wound_rel', 'pnc_visit_id', 'exist_wound_id', string='Existing wounds', required=True)
    
    medication_request_ids = fields.Many2many('product.template', 'rhs_pnc_visit_product_rel', 'pnc_visit_id', 'product_id', string='A set of medications')
    analysis_request_ids = fields.Many2many('product.template', 'rhs_pnc_visit_product_rel', 'pnc_visit_id', 'product_id', string='A set of tests')
    image_request_ids = fields.Many2many('product.template', 'rhs_pnc_visit_product_rel', 'pnc_visit_id', 'product_id', string='A set of x-rays')
    