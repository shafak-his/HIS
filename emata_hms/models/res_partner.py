from odoo import _, api, fields, models, exceptions, tools

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    is_patient = fields.Boolean('Is Patient')
    code = fields.Char('Patient Code')
    registration_date = fields.Date('Registration Date')
    first_name = fields.Char('First Name')
    last_name = fields.Char('Surname')
    father_name = fields.Char('Father Name')
    mother_name = fields.Char('Mother Name & Surname')
    birth_date = fields.Date('Birth Date')
    sex = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ], string='Sex')
    displacement_status = fields.Selection([
        ('displaced', 'Displaced'),
        ('resident', 'Resident'),
    ], string='Displacement Status')
    is_disability = fields.Boolean('Disability?')
    disability_type = fields.Selection([
        ('physical', 'Physical'),
        ('phsyco', 'Phsychological'),
    ], string='Disability Type')

    full_address = fields.Char('Full Address')
    original_location_id = fields.Many2one('em.location', string='Original Address')

    marital_status = fields.Selection([
        ('single', 'Single'),
        ('married', 'Married'),
        ('widowed', 'Widowed'),
        ('divorced', 'Divorced'),
    ], string='Marital Status')
    doc_number = fields.Char('Document Number')
    notes = fields.Char('Notes')

    medical_history_ids = fields.One2many('em.hms.medical.history', 'patient_id', string='Medical History')
    surgical_history_ids = fields.One2many('em.hms.surgical.history', 'patient_id', string='Surgical History')
    medication_history_ids = fields.One2many('em.hms.medication.history', 'patient_id', string='Medication History')
    allergic_history_ids = fields.One2many('em.hms.allergic.history', 'patient_id', string='Allergic History')

    @api.onchange('first_name', 'last_name')
    def _onchange_name_parts(self):
        self.name = " ".join(list(filter(None, [self.first_name, self.last_name])))

    def action_get_medication_requests(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Medication Requests',
            'view_mode': 'tree,form',
            'res_model': 'em.hms.medication.request.line',
            'domain': [('patient_id', '=', self.id)],
            'context': {'default_patient_id': self.id}
        }

    def action_get_analysis_requests(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Analysis Requests',
            'view_mode': 'tree,form',
            'res_model': 'em.hms.analysis.request',
            'domain': [('patient_id', '=', self.id)],
            'context': {'default_patient_id': self.id}
        }

    def action_get_image_requests(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Image Requests',
            'view_mode': 'tree,form',
            'res_model': 'em.hms.image.request',
            'domain': [('patient_id', '=', self.id)],
            'context': {'default_patient_id': self.id}
        }

    @api.model
    def create(self, vals):
        if vals.get('is_patient'):
            vals['code'] = self.sudo().env['ir.sequence'].next_by_code('em.patient.code')
        return super(ResPartner, self).create(vals)
    
    def write(self, vals):
        res = super(ResPartner, self).write(vals)
        if 'is_patient' in vals:
            for record in self:
                if not record.code:
                    record.write({'code': self.sudo().env['ir.sequence'].next_by_code('em.patient.code')})
        return res