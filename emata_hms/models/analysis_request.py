from odoo import _, api, fields, models, exceptions, tools

class EmHmsAnalysisRequest(models.Model):
    _name = 'em.hms.analysis.request'
    _description = 'Analysis Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    general_visit_id = fields.Many2one('em.hms.general.clinic.visit', string='General Visit')
    gynochological_visit_id = fields.Many2one('em.hms.gynochological.clinic.visit', string='Gynochological Visit')
    pnc_visit_id = fields.Many2one('em.hms.rhs.pnc.visit', string='PNC Visit')
    dial_urology_id = fields.Many2one('em.hms.dial.urology', string='Urology Visit')
    dial_nephrology_id = fields.Many2one('em.hms.dial.nephrology', string='Nephrology Visit')
    infertility_treatment_id = fields.Many2one('em.hms.rhs.infertility.treatment', string='Infertility Treatment')
    patient_admission_id = fields.Many2one('em.hms.patient.admission', string='Patient Admission')
    incubator_admission_id = fields.Many2one('em.hms.pediatric.incubator.admission', string='Incubator Admission')
    ward_admission_id = fields.Many2one('em.hms.pediatric.ward.admission', string='Ward Admission')
    pediatric_surgery_id = fields.Many2one('em.hms.pediatric.surgery', string='Pediatric Surgery')
    pediatric_clinic_id = fields.Many2one('em.hms.pediatric.clinic', string='Pediatric Clinic')
    pediatric_surgery_clinic_id = fields.Many2one('em.hms.pediatric.surgery.clinic', string='Pediatric Surgery Clinic')
    phototherapy_id = fields.Many2one('em.hms.pediatric.phototherapy', string='Phototherapy')
    icu_id = fields.Many2one('em.hms.pediatric.icu', string='ICU')
    nicu_id = fields.Many2one('em.hms.pediatric.nicu', string='NICU')
    hospitalization_id = fields.Many2one('em.hms.rhs.hospitalization', string='Hospitalization')
    rhs_surgery_id = fields.Many2one('em.hms.rhs.surgery', string='RHS Surgery')
    
    product_template_id = fields.Many2one('product.template', string='Product', domain="[('is_medical_analysis', '=', True)]", required=True)
    notes = fields.Char('Notes')