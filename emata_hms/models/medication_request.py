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

    product_template_id = fields.Many2one('product.template', string='Product', domain="[('is_medication', '=', True)]", required=True)
    uom_id = fields.Many2one('uom.uom', string='UoM', required=True)
    qty = fields.Float('Quantity', default=1)
    notes = fields.Char('Notes')

    @api.onchange('product_template_id')
    def _onchange_product_template_id(self):
        if self.product_template_id:
            self.uom_id = self.product_template_id.uom_id.id