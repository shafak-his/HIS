from odoo import _, api, fields, models, exceptions, tools


class EmHmsDialLithotripsy(models.Model):
    _name = 'em.hms.dial.lithotripsy'
    _description = 'Lithotripsy'
    _rec_name = 'patient_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    patient_id = fields.Many2one('res.partner', 'Patient Name', required=True, domain=[('is_patient','=',True)])
    visit_datetime = fields.Datetime('Visit Date/Time', required=True, tracking=True)
    weight = fields.Float('Weight', tracking=True)
    diagnosis_id = fields.Many2one('em.hms.icd10', string='Diagnosis', required=True, tracking=True)
    stone_location = fields.Selection([
        ('kidney', 'Kidney'),
        ('ureter', 'Ureter'),
        ('bladder', 'Bladder')
    ], string='Stone Location', tracking=True)

    session_type = fields.Selection([
        ('echo', 'ECHO'),
        ('ray', 'Ray')
    ], string='Session type', required=True, tracking=True)
    number_shots = fields.Integer('Number of Shots', required=True, tracking=True)
    notes = fields.Char('Notes', tracking=True)
    doctor_id = fields.Many2one('hr.employee', string='Doctor', tracking=True)
    company_id = fields.Many2one('res.company', 'Medical Center', default = lambda self: self.env.company)
