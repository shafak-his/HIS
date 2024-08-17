from odoo import models, fields, api, exceptions

class EmLocation(models.Model):
    _name = 'em.location'
    _description = 'Location'

    code = fields.Char('Code', required=True, tracking=True)
    name = fields.Char(string='Name', required=True, tracking=True)

    @api.depends('code', 'name')
    def name_get(self):
        res = []
        for record in self:
            name = f"{record.code} - {record.name}"
            res.append((record.id, name))
        return res