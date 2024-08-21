from odoo import _, api, fields, models, exceptions, tools


class EmHmsVitalSigns(models.Model):
    _name = 'em.hms.vital.signs'
    _description = 'Vital Signs Monitoring'
    _rec_name = 'patient_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    datetime = fields.Datetime('Time', required=True, tracking=True)
    delivery_id = fields.Many2one('em.hms.rhs.delivery', string='Delivery')
    patient_id = fields.Many2one('res.partner', 'Patient Name', required=True, domain=[('is_patient','=',True)])
    
    pressure = fields.Float('Pressure', required=True, tracking=True)
    pulse = fields.Float('Pulse', required=True, tracking=True)
    temperature = fields.Float('Temperature', required=True, tracking=True)
    awareness = fields.Char('Awareness')
    notes = fields.Char('Notes')

    company_id = fields.Many2one('res.company', 'Medical Center', default = lambda self: self.env.company)
    
    @api.onchange('delivery_id')
    def _onchange_delivery_id(self):
        self.patient_id = self.delivery_id.patient_id.id