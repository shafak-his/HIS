from odoo import _, api, fields, models, exceptions, tools

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    general_visit_id = fields.Many2one('em.hms.general.clinic.visit', string='General Clinic Visit')
    gynochological_visit_id = fields.Many2one('em.hms.rhs.gynochological.clinic.visit', string='Gynochological Visit')
    pnc_visit_id = fields.Many2one('em.hms.rhs.pnc.visit', string='PNC Visit')
    mh_gap_id = fields.Many2one('em.hms.mh.gap', string='MH Gap')
    dial_urology_id = fields.Many2one('em.hms.dial.urology', string='Urology Visit')
    dial_nephrology_id = fields.Many2one('em.hms.dial.nephrology', string='Nephrology Visit')
    infertility_treatment_id = fields.Many2one('em.hms.rhs.infertility.treatment', string='Infertility Treatment')
    patient_admission_id = fields.Many2one('em.hms.patient.admission', string='Patient Admission')
    pediatric_clinic_id = fields.Many2one('em.hms.pediatric.clinic', string='Pediatric Clinic')
    pediatric_surgery_clinic_id = fields.Many2one('em.hms.pediatric.surgery.clinic', string='Pediatric Surgery Clinic')
    icu_id = fields.Many2one('em.hms.pediatric.icu', string='ICU')
