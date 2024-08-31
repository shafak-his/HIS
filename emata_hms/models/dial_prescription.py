from odoo import _, api, fields, models, exceptions, tools
from pkg_resources import require

class EmHmsDay(models.Model):
    _name = 'em.hms.day'
    _description = 'Week days'
    _rec_name = 'name'

    name = fields.Char('Name', required=True)


class EmHmsDialPrescription(models.Model):
    _name = 'em.hms.dial.prescription'
    _description = 'Dialysis Prescription'
    _rec_name = 'patient_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    patient_id = fields.Many2one('res.partner', 'Patient Name', required=True, domain=[('is_patient','=',True)])
    prescription_datetime = fields.Datetime('Prescription Date/Time', required=True, tracking=True)
    day_ids = fields.Many2many('em.hms.day', 'dial_prescription_day_rel', 'dial_prescription_id', 'day_id', string='Dialysis days', required=True)
    duration = fields.Float('Dialysis duration', required=True)
    isolation = fields.Selection([
        ('need', 'Need isolation'),
        ('no_need', 'No isolation need')
    ], string='Isolation status', required=True, tracking=True)
    notes = fields.Char('Notes', tracking=True)
    doctor_id = fields.Many2one('hr.employee', string='Doctor', required=True, tracking=True)
    company_id = fields.Many2one('res.company', 'Medical Center', default = lambda self: self.env.company)
