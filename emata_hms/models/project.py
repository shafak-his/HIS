from odoo import _, api, fields, models, exceptions, tools

class ProjectProject(models.Model):
    _inherit = 'project.project'
    
    support_line_ids = fields.One2many('em.project.support.line', 'project_id', string='Support Lines')

class EmProjectSupportLine(models.Model):
    _name = 'em.project.support.line'
    _description = 'Project Support Line'
    
    project_id = fields.Many2one('project.project', string='Project', ondelete='cascade')
    company_ids = fields.Many2many('res.company', string='Centers', required=True)
    service_ids = fields.Many2many('em.hms.service', string='Services')
    clinic_ids = fields.Many2many('em.hms.clinic', string='Clinics')
    start_date = fields.Date('Start Date', required=True)
    end_date = fields.Date('End Date', required=True)

    @api.model
    def get_model_to_service_dict(self):
        return {
            'em.hms.general.clinic.visit': 'emata_hms.em_hms_service_clinic',
            'em.hms.rhs.surgery': 'emata_hms.em_hms_service_rhs',
            'em.hms.rhs.pnc': 'emata_hms.em_hms_service_rhs',
            'em.hms.rhs.pnc.visit': 'emata_hms.em_hms_service_rhs',
            'em.hms.rhs.postpartum.comp': 'emata_hms.em_hms_service_rhs',
            'em.hms.rhs.pathological.find': 'emata_hms.em_hms_service_rhs',
            'em.hms.rhs.infertility.treatment': 'emata_hms.em_hms_service_rhs',
            'em.hms.rhs.hospitalization': 'emata_hms.em_hms_service_rhs',
            'em.hms.rhs.hospitalization.monitoring': 'emata_hms.em_hms_service_rhs',
            'em.hms.rhs.fp': 'emata_hms.em_hms_service_rhs',
            'em.hms.rhs.fp.complaint': 'emata_hms.em_hms_service_rhs',
            'em.hms.rhs.fp.medical.history': 'emata_hms.em_hms_service_rhs',
            'em.hms.rhs.fp.pregnancy.check': 'emata_hms.em_hms_service_rhs',
            'em.hms.rhs.fp.problem': 'emata_hms.em_hms_service_rhs',
            'em.hms.rhs.edc': 'emata_hms.em_hms_service_rhs',
            'em.hms.rhs.edc.plan': 'emata_hms.em_hms_service_rhs',
            'em.hms.rhs.edc.ascus': 'emata_hms.em_hms_service_rhs',
            'em.hms.rhs.edc.sign': 'emata_hms.em_hms_service_rhs',
            'em.hms.rhs.edc.symptom': 'emata_hms.em_hms_service_rhs',
            'em.hms.rhs.edc.clinical.condition': 'emata_hms.em_hms_service_rhs',
            'em.hms.rhs.delivery': 'emata_hms.em_hms_service_rhs',
            'em.hms.rhs.anc': 'emata_hms.em_hms_service_rhs',
            'em.hms.rhs.anc.visit': 'emata_hms.em_hms_service_rhs',
            'em.hms.rhs.awareness': 'emata_hms.em_hms_service_rhs',
            'em.hms.rhs.gynochological.clinic.visit': 'emata_hms.em_hms_service_rhs',
            'em.hms.pediatric.ward.admission': 'emata_hms.em_hms_service_pediatric',
            'em.hms.pediatric.surgery': 'emata_hms.em_hms_service_pediatric',
            'em.hms.pediatric.surgery.clinic': 'emata_hms.em_hms_service_pediatric',
            'em.hms.pediatric.phototherapy': 'emata_hms.em_hms_service_pediatric',
            'em.hms.pediatric.nicu': 'emata_hms.em_hms_service_pediatric',
            'em.hms.pediatric.newborn.examination': 'emata_hms.em_hms_service_pediatric',
            'em.hms.pediatric.incubator.admission': 'emata_hms.em_hms_service_pediatric',
            'em.hms.pediatric.icu': 'emata_hms.em_hms_service_pediatric',
            'em.hms.pediatric.clinic': 'emata_hms.em_hms_service_pediatric',
            'em.hms.patient.admission': 'emata_hms.em_hms_service_patient_admission',
            'em.hms.patient.admission.visit': 'emata_hms.em_hms_service_patient_admission',
            'em.hms.patient.admission.surgery': 'emata_hms.em_hms_service_patient_admission',
            'em.hms.nutrition.stabilization.center': 'emata_hms.em_hms_service_nutrition',
            'em.hms.nutrition.screening.woman.topic': 'emata_hms.em_hms_service_nutrition',
            'em.hms.nutrition.screening.woman': 'emata_hms.em_hms_service_nutrition',
            'em.hms.nutrition.danger.sign.woman': 'emata_hms.em_hms_service_nutrition',
            'em.hms.nutrition.danger.sign.child': 'emata_hms.em_hms_service_nutrition',
            'em.hms.nutrition.screening.child': 'emata_hms.em_hms_service_nutrition',
            'em.hms.nutrition.group.session.bnf': 'emata_hms.em_hms_service_nutrition',
            'em.hms.nutrition.group.session.topic': 'emata_hms.em_hms_service_nutrition',
            'em.hms.nutrition.group.session': 'emata_hms.em_hms_service_nutrition',
            'em.hms.nutrition.bnf.visit': 'emata_hms.em_hms_service_nutrition',
            'em.hms.nutrition.topic': 'emata_hms.em_hms_service_nutrition',
            'em.hms.nutrition.team': 'emata_hms.em_hms_service_nutrition',
            'em.hms.necessity.giving': 'emata_hms.em_hms_service_mh',
            'em.hms.mh.referral': 'emata_hms.em_hms_service_mh',
            'em.hms.mh.pmplus': 'emata_hms.em_hms_service_mh',
            'em.hms.mh.gap': 'emata_hms.em_hms_service_mh',
            'em.hms.mh.awareness': 'emata_hms.em_hms_service_mh',
            'em.hms.dial.visit': 'emata_hms.em_hms_service_dial',
            'em.hms.dial.transfusion': 'emata_hms.em_hms_service_dial',
            'em.hms.dial.session.info': 'emata_hms.em_hms_service_dial',
            'em.hms.dial.urology': 'emata_hms.em_hms_service_dial',
            'em.hms.dial.prescription': 'emata_hms.em_hms_service_dial',
            'em.hms.dial.nephrology': 'emata_hms.em_hms_service_dial',
            'em.hms.dial.lithotripsy': 'emata_hms.em_hms_service_dial',
            'em.hms.dial.kidney.history': 'emata_hms.em_hms_service_dial',
            'em.hms.chw.individual.session': 'emata_hms.em_hms_service_chw',
            'em.hms.chw.group.session.bnf': 'emata_hms.em_hms_service_chw',
            'em.hms.chw.group.session': 'emata_hms.em_hms_service_chw',
        }
    
    @api.model
    def get_common_models(self):
        return [
            'em.hms.referral'
        ]

    @api.model
    def get_project_ids(self, company_id, model_name, clinic_id, operation_date):
        if not company_id:
            return self.env['project.project']

        domain = [('start_date', '<=', operation_date), ('end_date', '>=', operation_date),('company_ids', 'in', company_id.id)]

        common_models = self.get_common_models()
        if model_name not in common_models:
            service_ref = self.get_model_to_service_dict().get(model_name)
            if not service_ref:
                raise exceptions.ValidationError('Unsupported model! Contact technical support.')

            service_id = self.env.ref(service_ref)
            domain += [('service_ids', 'in', service_id.id)]

        if clinic_id:
            domain += ['|',('clinic_ids', 'in', clinic_id.id),('clinic_ids', '=', False)]

        records = self.search(domain)
        if not records:
            return self.env['project.project']
        return records.mapped('project_id')
