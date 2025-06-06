from odoo import _, api, fields, models, exceptions, tools


class EmHmsPatientAdmissionVisit(models.Model):
    _name = 'em.hms.patient.admission.visit'
    _description = 'Doctor Visit'
    _rec_name = 'patient_admission_id'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'em.common.form']

    patient_admission_id = fields.Many2one('em.hms.patient.admission', string='Patient Admission') # , required=True
    
    visit_datetime = fields.Datetime('Visit Date/Time', required=True, tracking=True)
    patient_id = fields.Many2one('res.partner', 'Patient Name', related='patient_admission_id.patient_id')
    doctor_id = fields.Many2one('hr.employee', 'Doctor', related='patient_admission_id.doctor_id')
    ward_nurse_id = fields.Many2one('hr.employee', string='Name Of The Ward Nurse', tracking=True)
    pulse = fields.Float('Pulse', tracking=True)
    oxygenation = fields.Float('Oxygenation', tracking=True)
    temperature = fields.Float('Body Temperature Measurement', tracking=True)
    urine = fields.Float('Urine', tracking=True)
    stool = fields.Float('Stool', tracking=True)
    notes = fields.Char('Notes', tracking=True)
    
    company_id = fields.Many2one('res.company', 'Medical Center', default = lambda self: self.env.company)
    
    _sql_constraints = [
        (
            'check_visit_datetime',
            'CHECK (visit_datetime <= NOW())',
            'Visit Date/Time Must Not Be Newer Than Now.'
        ),
    ]