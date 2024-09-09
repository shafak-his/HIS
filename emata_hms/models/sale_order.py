from odoo import _, api, fields, models, exceptions, tools

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    general_visit_id = fields.Many2one('em.hms.general.clinic.visit', string='General Clinic Visit')