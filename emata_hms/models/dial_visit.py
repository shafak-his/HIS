from odoo import _, api, fields, models, exceptions, tools

BLOOD_TYPES = [
    ('A+', 'A+'),
    ('B+', 'B+'),
    ('O+', 'O+'),
    ('AB+', 'AB+'),
    ('A-', 'A-'),
    ('B-', 'B-'),
    ('O-', 'O-'),
    ('AB-', 'AB-')
]

class EmHmsDialSessionInfo(models.Model):
    _name = 'em.hms.dial.session.info'
    _description = 'Session info'
    _rec_name = 'hour'

    dial_visit_id = fields.Many2one('em.hms.dial.visit', string='PNC', required=True)
    hour = fields.Selection([
        ('1st_hour', 'First hour'),
        ('2nd_hour', 'Second hour'),
        ('3rd_hour', 'Third hour')
    ], string='Hour', required=True, tracking=True)
    vp = fields.Float('VP')
    time = fields.Float('time')
    bp = fields.Float('BP')
    pulse = fields.Float('Pulse')
    temp = fields.Float('Temperature')
    ap = fields.Float('AP')
    tmp = fields.Float('TMP')


class EmHmsDialTransfusion(models.Model):
    _name = 'em.hms.dial.transfusion'
    _description = 'Transfusion'
    _rec_name = 'unit_number'

    dial_visit_id = fields.Many2one('em.hms.dial.visit', string='PNC', required=True)
    unit_number = fields.Char('Unit number', required=True)
    blood_donation_date = fields.Date('Blood donation date', tracking=True)
    expiry_date = fields.Date('Expiry date', tracking=True)
    patient_blood_group = fields.Selection(BLOOD_TYPES, string='Patient blood group', required=True, tracking=True)
    donor_blood_group = fields.Selection(BLOOD_TYPES, string='Donor blood group', required=True, tracking=True)



class EmHmsDialVisit(models.Model):
    _name = 'em.hms.dial.visit'
    _description = 'Dialysis visit'
    _rec_name = 'patient_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    patient_id = fields.Many2one('res.partner', 'Patient Name', required=True, domain=[('is_patient','=',True)])
    acceptance_date = fields.Date('Acceptance date', required=True, tracking=True)
    session_info_ids = fields.One2many('em.hms.dial.session.info', 'dial_visit_id', string='Session info', required=True)
    transfusion_ids = fields.One2many('em.hms.dial.transfusion', 'dial_visit_id', string='Transfusion', required=True)
    patient_condition = fields.Selection([
        ('sponsored', 'Sponsored'),
        ('emergency', 'Emergency'),
        ('death', 'Dropped because of death'),
        ('other_program', 'Dropped because in another program'),
        ('recovery', 'Dropped because of recovery')
    ], string='Hemodialysis patient condition', required=True, tracking=True)
    leaving_datetime = fields.Datetime('Leaving date', required=True, tracking=True)
    session_datetime = fields.Datetime('Session date', required=True, tracking=True)
    session_period = fields.Selection([
        ('1st_shift', 'First shift'),
        ('2nd_shift', 'Second shift'),
        ('3rd_shift', 'Third shift')
    ], string='Session period', required=True, tracking=True)
    technician_id = fields.Many2one('hr.employee', string='Technician name', required=True, tracking=True)
    dialysis_filter = fields.Selection([
        ('1.2', '1.2'),
        ('1.4', '1.4'),
        ('1.6', '1.6'),
        ('1.8', '1.8')
    ], string='Dialysis filter', required=True, tracking=True)
    dial_flow_rate = fields.Selection([
        ('500', '500'),
        ('800', '800')
    ], string='Dialysis flow rate', required=True, tracking=True)
    blood_flow_rate = fields.Float('Blood flow rate')
    erythropoietin_dose = fields.Integer('Erythropoietin dose')
    heparin_dose = fields.Integer('Heparin dose')
    other_medications = fields.Char('Other medications given', tracking=True)
    duration = fields.Float('Dialysis duration')
    fluid_concentration = fields.Float('fluid concentration')
    dry_weight = fields.Float('Dry weight')
    weight_after_session = fields.Float('Weight after session')
    dial_volume = fields.Float('Dialysis volume')
    doctor_notes = fields.Char('Doctor notes', tracking=True)
    technician_notes = fields.Char('Technician notes', tracking=True)
    doctor_id = fields.Many2one('hr.employee', string='Doctor', required=True, tracking=True)
    company_id = fields.Many2one('res.company', 'Medical Center', default = lambda self: self.env.company)
