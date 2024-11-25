from odoo import _, api, fields, models, exceptions, tools

class EmHmsMedicationRequest(models.Model):
    _name = 'em.hms.medication.request'
    _description = 'Medication Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    general_visit_id = fields.Many2one('em.hms.general.clinic.visit', string='General Visit')
    gynochological_visit_id = fields.Many2one('em.hms.gynochological.clinic.visit', string='Gynochological Visit')
    pnc_visit_id = fields.Many2one('em.hms.rhs.pnc.visit', string='PNC Visit')
    mh_gap_id = fields.Many2one('em.hms.mh.gap', string='MH Gap')
    dial_urology_id = fields.Many2one('em.hms.dial.urology', string='Urology Visit')
    dial_nephrology_id = fields.Many2one('em.hms.dial.nephrology', string='Nephrology Visit')
    infertility_treatment_id = fields.Many2one('em.hms.rhs.infertility.treatment', string='Infertility Treatment')
    patient_admission_id = fields.Many2one('em.hms.patient.admission', string='Patient Admission')
    pediatric_clinic_id = fields.Many2one('em.hms.pediatric.clinic', string='Pediatric Clinic')
    pediatric_surgery_clinic_id = fields.Many2one('em.hms.pediatric.surgery.clinic', string='Pediatric Surgery Clinic')
    icu_id = fields.Many2one('em.hms.pediatric.icu', string='ICU')
    hospitalization_id = fields.Many2one('em.hms.rhs.hospitalization', string='Hospitalization')
    rhs_surgery_id = fields.Many2one('em.hms.rhs.surgery', string='RHS Surgery')

    patient_id = fields.Many2one('res.partner', string='Patient', required=True)
    product_template_id = fields.Many2one('product.template', string='Product', domain="[('is_medication', '=', True)]", required=True)
    uom_id = fields.Many2one('uom.uom', string='UoM', required=True)
    qty = fields.Float('Quantity', default=1)
    notes = fields.Char('Notes')

    @api.onchange('product_template_id')
    def _onchange_product_template_id(self):
        if self.product_template_id:
            self.uom_id = self.product_template_id.uom_id.id

    def generate_sale_order(self, general_visit_id=False):
        patient_id = self[0].patient_id.id
        if any(record.patient_id.id != patient_id for record in self):
            raise exceptions.ValidationError('All requests must belong to the same patient!')

        order_line_vals = []
        for line in self:
            vals = {
                'display_type': False,
                'product_id': line.product_template_id.product_variant_id.id,
                'product_template_id': line.product_template_id.id,
                'name': line.product_template_id.name,
                'product_uom_qty': line.qty,
                'product_uom': line.uom_id.id,
                'price_unit': 0,
            }
            order_line_vals.append(vals)
            if line.notes:
                vals = {
                    'display_type': 'line_note',
                    'name': line.notes
                }
                order_line_vals.append(vals)

        first_record = self[0]
        sale_order = self.sudo().env['sale.order'].create({
            'general_visit_id': first_record.general_visit_id.id,
            'gynochological_visit_id': first_record.gynochological_visit_id.id,
            'pnc_visit_id': first_record.pnc_visit_id.id,
            'mh_gap_id': first_record.mh_gap_id.id,
            'dial_urology_id': first_record.dial_urology_id.id,
            'dial_nephrology_id': first_record.dial_nephrology_id.id,
            'infertility_treatment_id': first_record.infertility_treatment_id.id,
            'patient_admission_id': first_record.patient_admission_id.id,
            'pediatric_clinic_id': first_record.pediatric_clinic_id.id,
            'pediatric_surgery_clinic_id': first_record.pediatric_surgery_clinic_id.id,
            'icu_id': first_record.icu_id.id,
            'partner_id': first_record.patient_id.id,
            'date_order': fields.Date.today(),
            'order_line': [(0, 0, val) for val in order_line_vals]
        })

        sale_order.sudo().action_confirm()