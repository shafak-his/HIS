from odoo import _, api, fields, models, exceptions, tools


class EmHmsPhcClinicVisit(models.Model):
    _name = 'em.hms.phc.clinic.visit'
    _description = 'PHC Clinic Visit'
    _rec_name = 'visit_datetime'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    visit_datetime = fields.Datetime('Visit Date', required=True)
    
