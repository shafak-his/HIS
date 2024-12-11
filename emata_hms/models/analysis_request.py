from odoo import _, api, fields, models, exceptions, tools


class EmHmsAnalysisRequest(models.Model):
    _name = 'em.hms.analysis.request'
    _description = 'Analysis Request'
    _rec_name = 'patient_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    patient_id = fields.Many2one('res.partner', 'Patient Name', required=True, domain=[('is_patient','=',True)])
    name = fields.Char('Description')
    res_model_id = fields.Many2one('ir.model', 'Related Model')
    res_id = fields.Integer('Record ID')
    notes = fields.Char('Notes')

    line_ids = fields.One2many('em.hms.analysis.request.line', 'request_id', string='Lines')
    state = fields.Selection([
        ('draft', 'Pending'),
        ('done', 'Done'),
    ], string='Status', required=True, default='draft')

    def complete_order(self):
        self.write({
            'state': 'done'
        })

    def generate_order(self, related_record_id, line_ids):
        if not line_ids:
            return

        vals = {
            'patient_id': related_record_id.patient_id.id,
            'res_model_id': self.env['ir.model']._get(related_record_id._name).id,
            'res_id': related_record_id.id,
            'line_ids': [(4, l.id) for l in line_ids]
        }
        res = self.create(vals)
        return res

class EmHmsAnalysisRequestLine(models.Model):
    _name = 'em.hms.analysis.request.line'
    _description = 'Analysis Request Line'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    request_id = fields.Many2one('em.hms.analysis.request', string='Request', ondelete='cascade')

    general_visit_id = fields.Many2one('em.hms.general.clinic.visit', string='General Visit')
    gynochological_visit_id = fields.Many2one('em.hms.rhs.gynochological.clinic.visit', string='Gynochological Visit')
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