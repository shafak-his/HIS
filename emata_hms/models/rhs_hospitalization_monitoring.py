from odoo import _, api, fields, models, exceptions, tools


class EmHmsRHSDeliveryLabor(models.Model):
    _name = 'em.hms.rhs.hospitalization.monitoring'
    _description = 'Labor Monitoring'
    _rec_name = 'hospitalization_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    hospitalization_id = fields.Many2one('em.hms.rhs.hospitalization', string='Delivery', required=True)
    patient_id = fields.Many2one('res.partner', 'Patient Name', related='hospitalization_id.patient_id')
    monitoring_time = fields.Datetime('Time', tracking=True)
    pressure = fields.Float('Pressure', tracking=True)
    pulse = fields.Float('Pulse', tracking=True)
    temperature = fields.Float('Temperature', tracking=True)
    is_urinary_output = fields.Boolean('Urinary Output', tracking=True)
    notes = fields.Char('Notes', tracking=True)
    
    company_id = fields.Many2one('res.company', 'Medical Center', default = lambda self: self.env.company)
    project_id = fields.Many2one('project.project', string='Project', tracking=True)
    allowed_project_ids = fields.Many2many('project.project', compute='_compute_allowed_project_ids', string='Allowed Projects', compute_sudo=True)

    @api.onchange('allowed_project_ids')
    def _onchange_allowed_project_ids(self):
        if self.allowed_project_ids:
            self.project_id = self.allowed_project_ids[0].id

    @api.depends('company_id')
    def _compute_allowed_project_ids(self):
        for record in self:
            record.allowed_project_ids = self.env['em.project.support.line'].get_project_ids(record.company_id, self._name, False, fields.Date.today()).ids
    
    