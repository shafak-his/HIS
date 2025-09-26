from odoo import _, api, fields, models, exceptions

class EmBaseCommonForm(models.AbstractModel):
    _name = 'em.base.common.form'
    _description = 'Base Common Form'

    project_id = fields.Many2one('project.project', string='Project', tracking=True)
    allowed_project_ids = fields.Many2many('project.project', compute='_compute_allowed_project_ids', string='Allowed Projects', compute_sudo=True)

    @api.onchange('allowed_project_ids')
    def _onchange_allowed_project_ids(self):
        if self.allowed_project_ids:
            self.project_id = self.allowed_project_ids[0].id
        else:
            self.project_id = False

    @api.depends('company_id')
    def _compute_allowed_project_ids(self):
        for record in self:
            record.allowed_project_ids = self.env['em.project.support.line'].get_project_ids(record.company_id, self._name, False, fields.Date.today()).ids

class EmCommonForm(models.AbstractModel):
    _name = 'em.common.form'
    _description = 'Common Form'
    _inherit = ['em.base.common.form']

    bnf_status = fields.Selection([
        ('new', 'New'),
        ('old', 'Old')
    ], string='BNF Status', tracking=True)

    def _update_bnf_status(self):
        self.ensure_one()
        if 'patient_id' not in self._fields:
            return

        common_models = self.env['em.project.support.line'].get_common_models()
        if self._name not in common_models:
            model_to_service_dict = self.env['em.project.support.line'].get_model_to_service_dict()
            service_name = model_to_service_dict.get(self._name)
            if not service_name:
                raise exceptions.ValidationError('Unsupported form to determine the BNF status! Contact the technical support.')
            
            same_service_models = [k for k, v in model_to_service_dict.items() if v == service_name]
        else:
            same_service_models = [self._name]

        for model_name in same_service_models:
            if 'patient_id' not in self.env[model_name]._fields:
                continue

            domain = [('project_id', '=', self.project_id.id),('patient_id', '=', self.patient_id.id)]
            if model_name == self._name:
                domain += [('id', '!=', self.id)]
            if self.env[model_name].search(domain):
                self.write({'bnf_status': 'old'})
                return

        self.write({'bnf_status': 'new'})

    @api.model
    def create(self, vals):
        res = super(EmCommonForm, self).create(vals)
        res._update_bnf_status()
        return res

    def write(self, vals):
        res = super(EmCommonForm, self).write(vals)
        if 'project_id' in vals:
            for record in self:
                record._update_bnf_status()
        return res