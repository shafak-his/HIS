from odoo import _, api, fields, models, exceptions, tools


class EmHmsPhcClinic(models.Model):
    _name = 'em.hms.phc.clinic'
    _description = 'PHC Clinic'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char('Clinic name', required=True)
    name_lang = fields.Char('Clinic Arabic name', required=True)
    