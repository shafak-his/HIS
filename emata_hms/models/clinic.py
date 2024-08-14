from odoo import _, api, fields, models, exceptions, tools


class EmHmsClinic(models.Model):
    _name = 'em.hms.clinic'
    _description = 'Clinic'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char('Clinic Name', required=True)
    name_lang = fields.Char('Clinic Arabic Name', required=True)
    