from odoo import models, fields, api, exceptions

class CountryState(models.Model):
    _inherit = 'res.country.state'

    name = fields.Char(translate=True)

class EmCountryDistrict(models.Model):
    _name = 'em.country.district'
    _description = 'District'

    name = fields.Char(string='Name', required=True, tracking=True, translate=True)
    state_id = fields.Many2one('res.country.state', string='State')

class EmCountrySubDistrict(models.Model):
    _name = 'em.country.sub.district'
    _description = 'Sub-District'

    name = fields.Char(string='Name', required=True, tracking=True, translate=True)
    district_id = fields.Many2one('em.country.district', string='District')

class EmLocation(models.Model):
    _name = 'em.location'
    _description = 'Location'

    code = fields.Char('Code', required=True, tracking=True)
    name = fields.Char(string='Name', required=True, tracking=True, translate=True)
    sub_district_id = fields.Many2one('em.country.sub.district', string='Sub-District')

    @api.depends('code', 'name')
    def name_get(self):
        res = []
        for record in self:
            name = f"{record.code} - {record.name}"
            res.append((record.id, name))
        return res