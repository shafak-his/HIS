from odoo import _, api, fields, models, exceptions, tools
from odoo.osv import expression

class EmHmsICD10(models.Model):
    _name = 'em.hms.icd10'
    _description = 'ICD10'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    code = fields.Char('Code', required=True)
    name = fields.Char('Diagnosis name', required=True, translate=True)
    is_ncd = fields.Boolean('Is NCD')
    is_traumatic = fields.Boolean('Is Traumatic')
    is_diabetes = fields.Boolean('Is Diabetes')
    
    @api.model
    def _name_search(self, name, domain=None, operator='ilike', limit=100, order=None):
        if name and operator in ('=', 'ilike', '=ilike', 'like', '=like'):
            domain = domain or []
            name_domain = ['|',
                ('name', operator, name),
                ('code', operator, name),
            ]
            partner_ids = self._search(expression.AND([name_domain, domain]), limit=limit, order=order)
            return partner_ids
        return super(EmHmsICD10, self)._name_search(name=name, domain=domain, operator=operator, limit=limit, order=order)