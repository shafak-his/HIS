from odoo import _, api, fields, models, exceptions, tools


class EmHmsImageRequest(models.Model):
    _name = 'em.hms.image.request'
    _description = 'image Request'
    _rec_name = 'patient_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    patient_id = fields.Many2one('res.partner', 'Patient Name', required=True, domain=[('is_patient','=',True)])
    name = fields.Char('Description')
    res_model_id = fields.Many2one('ir.model', 'Related Model')
    res_id = fields.Integer('Record ID')
    notes = fields.Char('Notes')
    state = fields.Selection([
        ('draft', 'Pending'),
        ('done', 'Done'),
    ], string='Status', required=True, default='draft')

    line_ids = fields.One2many('em.hms.image.request.line', 'request_id', string='Lines')

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

class EmHmsImageRequestLine(models.Model):
    _name = 'em.hms.image.request.line'
    _description = 'Image Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    request_id = fields.Many2one('em.hms.image.request', string='Request', ondelete='cascade')

    general_visit_id = fields.Many2one('em.hms.general.clinic.visit', string='General Visit')
    gynochological_visit_id = fields.Many2one('em.hms.gynochological.clinic.visit', string='Gynochological Visit')
    pnc_visit_id = fields.Many2one('em.hms.rhs.pnc.visit', string='PNC Visit')
    dial_urology_id = fields.Many2one('em.hms.dial.urology', string='Urology Visit')
    dial_nephrology_id = fields.Many2one('em.hms.dial.nephrology', string='Nephrology Visit')
    patient_admission_id = fields.Many2one('em.hms.patient.admission', string='Patient Admission')
    incubator_admission_id = fields.Many2one('em.hms.pediatric.incubator.admission', string='Incubator Admission')
    ward_admission_id = fields.Many2one('em.hms.pediatric.ward.admission', string='Ward Admission')
    pediatric_surgery_id = fields.Many2one('em.hms.pediatric.surgery', string='Pediatric Surgery')
    pediatric_clinic_id = fields.Many2one('em.hms.pediatric.clinic', string='Pediatric Clinic')
    pediatric_surgery_clinic_id = fields.Many2one('em.hms.pediatric.surgery.clinic', string='Pediatric Surgery Clinic')
    phototherapy_id = fields.Many2one('em.hms.pediatric.phototherapy', string='Phototherapy')
    icu_id = fields.Many2one('em.hms.pediatric.icu', string='ICU')
    nicu_id = fields.Many2one('em.hms.pediatric.nicu', string='NICU')

    product_template_id = fields.Many2one('product.template', string='Product', domain="[('is_medical_imaging', '=', True)]", required=True)
    notes = fields.Char('Notes')