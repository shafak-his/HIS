from odoo import _, api, fields, models, exceptions, tools

class PreviousObstetricHistory(models.Model):
  _name = 'em.hms.rhs.anc.previous.obstetric'
  _description = 'Previous Obstetric History'
  _rec_name = 'previous_obstetrich_history_id'
  _inherit = ['mail.thread', 'mail.activity.mixin']
  

  previous_obstetrich_history_id = fields.Many2one('em.hms.rhs.anc', string='Previous Obstetrich History', required=True)
  patient_id = fields.Many2one('res.partner', 'Patient Name', related='previous_obstetrich_history_id.patient_id')
  previou_pregnancies_count = fields.Integer('# Pregnancies', tracking=True , default =1)
  type_of_previous_births = fields.Selection([
        ('liveborn', 'Liveborn'),
        ('premature', 'Premature'),
        ('miscarriage', 'Miscarriage'),
        ('stillborn', 'Stillborn')
        ], string='Type Of Previous Births', tracking=True)
  nature_of_previous_birth = fields.Selection([
       ('natural', 'Natural'),
        ('cesarean', 'Cesarean'),
        ('aided', 'Aided')
        ], string='Nature Of Previous Births', tracking=True)
  is_deformities = fields.Boolean('is Deformities', tracking=True)
  additional_notes = fields.Char('Additional_notes', tracking=True)
  company_id = fields.Many2one('res.company', 'Medical Center', default = lambda self: self.env.company)