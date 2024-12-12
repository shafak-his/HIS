from odoo import _, api, fields, models, exceptions, tools


class EmHmsRHSDeliveryLabor(models.Model):
    _name = 'em.hms.rhs.hospitalization.monitoring'
    _description = 'Labor Monitoring'
    _rec_name = 'hospitalization_id'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'em.common.form']
    
    hospitalization_id = fields.Many2one('em.hms.rhs.hospitalization', string='Delivery', required=True)
    patient_id = fields.Many2one('res.partner', 'Patient Name', related='hospitalization_id.patient_id')
    monitoring_time = fields.Datetime('Time', tracking=True)
    pressure = fields.Float('Pressure', tracking=True)
    pulse = fields.Float('Pulse', tracking=True)
    temperature = fields.Float('Temperature', tracking=True)
    is_urinary_output = fields.Boolean('Urinary Output', tracking=True)
    notes = fields.Char('Notes', tracking=True)
    
    company_id = fields.Many2one('res.company', 'Medical Center', default = lambda self: self.env.company)