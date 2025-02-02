from odoo import _, api, fields, models, exceptions, tools


class EmHmsClinic(models.Model):
    _name = 'em.hms.clinic'
    _description = 'Clinic'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char('Clinic Name', required=True, translate=True)
    company_ids = fields.Many2many('res.company', string='Centers', required=True, default=lambda self: self.env.company.ids)
    
class EmHmsService(models.Model):
    _name = 'em.hms.service'
    _description = 'HMS Service'
    
    name = fields.Char('Name', required=True)