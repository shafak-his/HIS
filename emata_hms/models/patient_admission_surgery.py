from odoo import _, api, fields, models, exceptions, tools


class EmHmsPatientAdmissionSurgery(models.Model):
    _name = 'em.hms.patient.admission.surgery'
    _description = 'Surgery'
    _rec_name = 'patient_admission_id'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'em.common.form']

    patient_admission_id = fields.Many2one('em.hms.patient.admission', string='Patient Admission') # , required=True
    patient_id = fields.Many2one('res.partner', 'Patient Name', related='patient_admission_id.patient_id')
    
    surgery_date = fields.Date('Date Of Surgery', required=True, tracking=True)
    surgery_type = fields.Selection([
        ('ambulance', 'Ambulance'),
        ('election', 'Election')
    ], string='Type Of Surgery', tracking=True)
    surgical_classification = fields.Selection([
        ('major_Surgery', 'Major Surgery'),
        ('minor_Surgery', 'Minor Surgery')
    ], string='Surgical Classification', tracking=True)
    surgical_specialty = fields.Selection([
        ('bone', 'Bone'),
        ('general', 'General')
    ], string='Surgical Specialty', tracking=True)
    bone_surgical_procedure_id = fields.Many2one('em.hms.surgical.procedure', string='Surgical Procedure For Bone', domain=[('subcategory_id.category','=','bone')], tracking=True)
    general_surgical_procedure_id = fields.Many2one('em.hms.surgical.procedure', string='Surgical Procedure For General', domain=[('subcategory_id.category','=','general')], tracking=True)
    anesthesia_type = fields.Selection([
        ('general_anesthesia', 'General Anesthesia'),
        ('local_anesthesia', 'Local Anesthesia')
    ], string='Type Of Anesthesia', tracking=True)
    anesthesia_technician_id = fields.Many2one('hr.employee', string='Name Of Anesthesia Technician', tracking=True)
    surgical_report = fields.Char('Surgical Report', tracking=True)
    anesthesia_report = fields.Char('Anesthesia Report During Surgery', tracking=True)
    notes = fields.Char('Notes', tracking=True)
    
    company_id = fields.Many2one('res.company', 'Medical Center', default = lambda self: self.env.company)
    
    _sql_constraints = [
        ('check_surgery_date', 'CHECK (surgery_date <= CURRENT_DATE)', 'Surgery Date Must Not Be Newer Than Today.'),
    ]