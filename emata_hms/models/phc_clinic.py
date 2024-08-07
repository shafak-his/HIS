from odoo import _, api, fields, models, exceptions, tools


class EmHmsPhcClinic(models.Model):
    _name = 'em.hms.phc.clinic'
    _description = 'PHC Clinic'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Datetime('Clinic name', required=True)
    name_lang = fields.Datetime('Clinic Arabic name', required=True)
    
