from odoo import _, api, fields, models, exceptions, tools
from odoo.osv import expression

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    is_patient = fields.Boolean('Is Patient')
    code = fields.Char('Patient Code')
    registration_date = fields.Date('Registration Date')
    first_name = fields.Char('First Name')
    last_name = fields.Char('Surname')
    father_name = fields.Char('Father Name')
    mother_name = fields.Char('Mother Name & Surname')
    birth_date = fields.Date('Birth Date')
    sex = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ], string='Sex')
    displacement_status = fields.Selection([
        ('displaced', 'Displaced'),
        ('resident', 'Resident'),
    ], string='Displacement Status')
    is_disability = fields.Boolean('Disability?')
    disability_type = fields.Selection([
        ('physical', 'Physical'),
        ('phsyco', 'Phsychological'),
    ], string='Disability Type')

    full_address = fields.Char('Full Address')
    original_location_id = fields.Many2one('em.location', string='Original Address')
    original_location =fields.Char('Original Address')
    marital_status = fields.Selection([
        ('single', 'Single'),
        ('married', 'Married'),
        ('widowed', 'Widowed'),
        ('divorced', 'Divorced'),
    ], string='Marital Status')
    doc_number = fields.Char('Document Number')
    notes = fields.Char('Notes')

    medical_history_ids = fields.One2many('em.hms.medical.history', 'patient_id', string='Medical History')
    surgical_history_ids = fields.One2many('em.hms.surgical.history', 'patient_id', string='Surgical History')
    medication_history_ids = fields.One2many('em.hms.medication.history', 'patient_id', string='Medication History')
    allergic_history_ids = fields.One2many('em.hms.allergic.history', 'patient_id', string='Allergic History')

    # services
    chw_individual_session_ids = fields.One2many('em.hms.chw.individual.session', 'patient_id')
    chw_individual_session_count = fields.Integer(compute='_compute_chw_individual_session_count', compute_sudo=True)

    dial_kidney_history_ids = fields.One2many('em.hms.dial.kidney.history', 'patient_id')
    dial_kidney_history_count = fields.Integer(compute='_compute_dial_kidney_history_count', compute_sudo=True)

    dial_lithotripsy_ids = fields.One2many('em.hms.dial.lithotripsy', 'patient_id')
    dial_lithotripsy_count = fields.Integer(compute='_compute_dial_lithotripsy_count', compute_sudo=True)

    dial_nephrology_ids = fields.One2many('em.hms.dial.nephrology', 'patient_id')
    dial_nephrology_count = fields.Integer(compute='_compute_dial_nephrology_count', compute_sudo=True)

    dial_prescription_ids = fields.One2many('em.hms.dial.prescription', 'patient_id')
    dial_prescription_count = fields.Integer(compute='_compute_dial_prescription_count', compute_sudo=True)

    dial_urology_ids = fields.One2many('em.hms.dial.urology', 'patient_id')
    dial_urology_count = fields.Integer(compute='_compute_dial_urology_count', compute_sudo=True)

    dial_visit_ids = fields.One2many('em.hms.dial.visit', 'patient_id')
    dial_visit_count = fields.Integer(compute='_compute_dial_visit_count', compute_sudo=True)

    mh_gap_ids = fields.One2many('em.hms.mh.gap', 'patient_id')
    mh_gap_count = fields.Integer(compute='_compute_mh_gap_count', compute_sudo=True)

    mh_pmplus_ids = fields.One2many('em.hms.mh.pmplus', 'patient_id')
    mh_pmplus_count = fields.Integer(compute='_compute_mh_pmplus_count', compute_sudo=True)

    mh_referral_ids = fields.One2many('em.hms.mh.referral', 'patient_id')
    mh_referral_count = fields.Integer(compute='_compute_mh_referral_count', compute_sudo=True)

    necessity_giving_ids = fields.One2many('em.hms.necessity.giving', 'patient_id')
    necessity_giving_count = fields.Integer(compute='_compute_necessity_giving_count', compute_sudo=True)

    nutrition_screening_child_ids = fields.One2many('em.hms.nutrition.screening.child', 'patient_id')
    nutrition_screening_child_count = fields.Integer(compute='_compute_nutrition_screening_child_count', compute_sudo=True)

    nutrition_screening_woman_ids = fields.One2many('em.hms.nutrition.screening.woman', 'patient_id')
    nutrition_screening_woman_count = fields.Integer(compute='_compute_nutrition_screening_woman_count', compute_sudo=True)

    nutrition_stabilization_center_ids = fields.One2many('em.hms.nutrition.stabilization.center', 'patient_id')
    nutrition_stabilization_center_count = fields.Integer(compute='_compute_nutrition_stabilization_center_count', compute_sudo=True)

    patient_admission_surgery_ids = fields.One2many('em.hms.patient.admission.surgery', 'patient_id')
    patient_admission_surgery_count = fields.Integer(compute='_compute_patient_admission_surgery_count', compute_sudo=True)

    patient_admission_visit_ids = fields.One2many('em.hms.patient.admission.visit', 'patient_id')
    patient_admission_visit_count = fields.Integer(compute='_compute_patient_admission_visit_count', compute_sudo=True)

    patient_admission_ids = fields.One2many('em.hms.patient.admission', 'patient_id')
    patient_admission_count = fields.Integer(compute='_compute_patient_admission_count', compute_sudo=True)

    pediatric_clinic_ids = fields.One2many('em.hms.pediatric.clinic', 'patient_id')
    pediatric_clinic_count = fields.Integer(compute='_compute_pediatric_clinic_count', compute_sudo=True)

    pediatric_icu_ids = fields.One2many('em.hms.pediatric.icu', 'patient_id')
    pediatric_icu_count = fields.Integer(compute='_compute_pediatric_icu_count', compute_sudo=True)

    pediatric_incubator_admission_ids = fields.One2many('em.hms.pediatric.incubator.admission', 'patient_id')
    pediatric_incubator_admission_count = fields.Integer(compute='_compute_pediatric_incubator_admission_count', compute_sudo=True)

    pediatric_newborn_examination_ids = fields.One2many('em.hms.pediatric.newborn.examination', 'patient_id')
    pediatric_newborn_examination_count = fields.Integer(compute='_compute_pediatric_newborn_examination_count', compute_sudo=True)

    pediatric_nicu_ids = fields.One2many('em.hms.pediatric.nicu', 'patient_id')
    pediatric_nicu_count = fields.Integer(compute='_compute_pediatric_nicu_count', compute_sudo=True)

    pediatric_phototherapy_ids = fields.One2many('em.hms.pediatric.phototherapy', 'patient_id')
    pediatric_phototherapy_count = fields.Integer(compute='_compute_pediatric_phototherapy_count', compute_sudo=True)

    pediatric_surgery_clinic_ids = fields.One2many('em.hms.pediatric.surgery.clinic', 'patient_id')
    pediatric_surgery_clinic_count = fields.Integer(compute='_compute_pediatric_surgery_clinic_count', compute_sudo=True)

    pediatric_surgery_ids = fields.One2many('em.hms.pediatric.surgery', 'patient_id')
    pediatric_surgery_count = fields.Integer(compute='_compute_pediatric_surgery_count', compute_sudo=True)

    pediatric_ward_admission_ids = fields.One2many('em.hms.pediatric.ward.admission', 'patient_id')
    pediatric_ward_admission_count = fields.Integer(compute='_compute_pediatric_ward_admission_count', compute_sudo=True)

    rhs_gynochological_clinic_visit_ids = fields.One2many('em.hms.rhs.gynochological.clinic.visit', 'patient_id')
    rhs_gynochological_clinic_visit_count = fields.Integer(compute='_compute_rhs_gynochological_clinic_visit_count', compute_sudo=True)

    rhs_awareness_ids = fields.One2many('em.hms.rhs.awareness', 'patient_id')
    rhs_awareness_count = fields.Integer(compute='_compute_rhs_awareness_count', compute_sudo=True)

    rhs_anc_visit_ids = fields.One2many('em.hms.rhs.anc.visit', 'patient_id')
    rhs_anc_visit_count = fields.Integer(compute='_compute_rhs_anc_visit_count', compute_sudo=True)

    rhs_anc_ids = fields.One2many('em.hms.rhs.anc', 'patient_id')
    rhs_anc_count = fields.Integer(compute='_compute_rhs_anc_count', compute_sudo=True)

    rhs_delivery_ids = fields.One2many('em.hms.rhs.delivery', 'patient_id')
    rhs_delivery_count = fields.Integer(compute='_compute_rhs_delivery_count', compute_sudo=True)

    rhs_edc_ids = fields.One2many('em.hms.rhs.edc', 'patient_id')
    rhs_edc_count = fields.Integer(compute='_compute_rhs_edc_count', compute_sudo=True)

    rhs_fp_ids = fields.One2many('em.hms.rhs.fp', 'patient_id')
    rhs_fp_count = fields.Integer(compute='_compute_rhs_fp_count', compute_sudo=True)

    rhs_hospitalization_monitoring_ids = fields.One2many('em.hms.rhs.hospitalization.monitoring', 'patient_id')
    rhs_hospitalization_monitoring_count = fields.Integer(compute='_compute_rhs_hospitalization_monitoring_count', compute_sudo=True)

    rhs_hospitalization_ids = fields.One2many('em.hms.rhs.hospitalization', 'patient_id')
    rhs_hospitalization_count = fields.Integer(compute='_compute_rhs_hospitalization_count', compute_sudo=True)

    rhs_infertility_treatment_ids = fields.One2many('em.hms.rhs.infertility.treatment', 'patient_id')
    rhs_infertility_treatment_count = fields.Integer(compute='_compute_rhs_infertility_treatment_count', compute_sudo=True)

    rhs_pnc_visit_ids = fields.One2many('em.hms.rhs.pnc.visit', 'patient_id')
    rhs_pnc_visit_count = fields.Integer(compute='_compute_rhs_pnc_visit_count', compute_sudo=True)

    rhs_pnc_ids = fields.One2many('em.hms.rhs.pnc', 'patient_id')
    rhs_pnc_count = fields.Integer(compute='_compute_rhs_pnc_count', compute_sudo=True)

    rhs_surgery_ids = fields.One2many('em.hms.rhs.surgery', 'patient_id')
    rhs_surgery_count = fields.Integer(compute='_compute_rhs_surgery_count', compute_sudo=True)

    general_clinic_visit_ids = fields.One2many('em.hms.general.clinic.visit', 'patient_id')
    general_clinic_visit_count = fields.Integer(compute='_compute_general_clinic_visit_count', compute_sudo=True)


    @api.onchange('first_name','father_name', 'last_name')
    def _onchange_name_parts(self):
        self.name = " ".join(list(filter(None, [self.first_name, self.father_name, self.last_name])))

    @api.depends('complete_name', 'email', 'vat', 'state_id', 'country_id', 'commercial_company_name')
    @api.depends_context('show_address', 'partner_show_db_id', 'address_inline', 'show_email', 'show_vat', 'lang')
    def _compute_display_name(self):
        super(ResPartner, self)._compute_display_name()
        for partner in self:
            name = partner.name
            if partner.code:
                name = f"{partner.code} - {partner.name}"
            partner.display_name = name

    @api.model
    def _name_search(self, name, domain=None, operator='ilike', limit=100, order=None):
        if name and operator in ('=', 'ilike', '=ilike', 'like', '=like'):
            domain = domain or []
            name_domain = ['|','|','|','|',
                ('name', operator, name),
                ('code', operator, name),
                ('email', operator, name),
                ('mobile', operator, name),
                ('doc_number', operator, name),
            ]
            partner_ids = self._search(expression.AND([name_domain, domain]), limit=limit, order=order)
            return partner_ids
        return super(ResPartner, self)._name_search(name=name, domain=domain, operator=operator, limit=limit, order=order)

    def action_get_medication_requests(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Medication Requests',
            'view_mode': 'tree,form',
            'res_model': 'em.hms.medication.request.line',
            'domain': [('patient_id', '=', self.id)],
            'context': {'default_patient_id': self.id}
        }

    def action_get_analysis_requests(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Analysis Requests',
            'view_mode': 'tree,form',
            'res_model': 'em.hms.analysis.request',
            'domain': [('patient_id', '=', self.id)],
            'context': {'default_patient_id': self.id}
        }

    def action_get_image_requests(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Image Requests',
            'view_mode': 'tree,form',
            'res_model': 'em.hms.image.request',
            'domain': [('patient_id', '=', self.id)],
            'context': {'default_patient_id': self.id}
        }

    @api.model
    def create(self, vals):
        if vals.get('is_patient'):
            vals['code'] = self.sudo().env['ir.sequence'].next_by_code('em.patient.code')
        return super(ResPartner, self).create(vals)
    
    def write(self, vals):
        res = super(ResPartner, self).write(vals)
        if 'is_patient' in vals:
            for record in self:
                if not record.code:
                    record.write({'code': self.sudo().env['ir.sequence'].next_by_code('em.patient.code')})
        return res

    # services
    @api.depends('chw_individual_session_ids')
    def _compute_chw_individual_session_count(self):
        for record in self:
            record.chw_individual_session_count = len(record.chw_individual_session_ids)

    @api.depends('dial_kidney_history_ids')
    def _compute_dial_kidney_history_count(self):
        for record in self:
            record.dial_kidney_history_count = len(record.dial_kidney_history_ids)

    @api.depends('dial_lithotripsy_ids')
    def _compute_dial_lithotripsy_count(self):
        for record in self:
            record.dial_lithotripsy_count = len(record.dial_lithotripsy_ids)

    @api.depends('dial_nephrology_ids')
    def _compute_dial_nephrology_count(self):
        for record in self:
            record.dial_nephrology_count = len(record.dial_nephrology_ids)

    @api.depends('dial_prescription_ids')
    def _compute_dial_prescription_count(self):
        for record in self:
            record.dial_prescription_count = len(record.dial_prescription_ids)

    @api.depends('dial_urology_ids')
    def _compute_dial_urology_count(self):
        for record in self:
            record.dial_urology_count = len(record.dial_urology_ids)

    @api.depends('dial_visit_ids')
    def _compute_dial_visit_count(self):
        for record in self:
            record.dial_visit_count = len(record.dial_visit_ids)

    @api.depends('mh_gap_ids')
    def _compute_mh_gap_count(self):
        for record in self:
            record.mh_gap_count = len(record.mh_gap_ids)

    @api.depends('mh_pmplus_ids')
    def _compute_mh_pmplus_count(self):
        for record in self:
            record.mh_pmplus_count = len(record.mh_pmplus_ids)

    @api.depends('mh_referral_ids')
    def _compute_mh_referral_count(self):
        for record in self:
            record.mh_referral_count = len(record.mh_referral_ids)

    @api.depends('necessity_giving_ids')
    def _compute_necessity_giving_count(self):
        for record in self:
            record.necessity_giving_count = len(record.necessity_giving_ids)

    @api.depends('nutrition_screening_child_ids')
    def _compute_nutrition_screening_child_count(self):
        for record in self:
            record.nutrition_screening_child_count = len(record.nutrition_screening_child_ids)

    @api.depends('nutrition_screening_woman_ids')
    def _compute_nutrition_screening_woman_count(self):
        for record in self:
            record.nutrition_screening_woman_count = len(record.nutrition_screening_woman_ids)

    @api.depends('nutrition_stabilization_center_ids')
    def _compute_nutrition_stabilization_center_count(self):
        for record in self:
            record.nutrition_stabilization_center_count = len(record.nutrition_stabilization_center_ids)

    @api.depends('patient_admission_surgery_ids')
    def _compute_patient_admission_surgery_count(self):
        for record in self:
            record.patient_admission_surgery_count = len(record.patient_admission_surgery_ids)

    @api.depends('patient_admission_visit_ids')
    def _compute_patient_admission_visit_count(self):
        for record in self:
            record.patient_admission_visit_count = len(record.patient_admission_visit_ids)

    @api.depends('patient_admission_ids')
    def _compute_patient_admission_count(self):
        for record in self:
            record.patient_admission_count = len(record.patient_admission_ids)

    @api.depends('pediatric_clinic_ids')
    def _compute_pediatric_clinic_count(self):
        for record in self:
            record.pediatric_clinic_count = len(record.pediatric_clinic_ids)

    @api.depends('pediatric_icu_ids')
    def _compute_pediatric_icu_count(self):
        for record in self:
            record.pediatric_icu_count = len(record.pediatric_icu_ids)

    @api.depends('pediatric_incubator_admission_ids')
    def _compute_pediatric_incubator_admission_count(self):
        for record in self:
            record.pediatric_incubator_admission_count = len(record.pediatric_incubator_admission_ids)

    @api.depends('pediatric_newborn_examination_ids')
    def _compute_pediatric_newborn_examination_count(self):
        for record in self:
            record.pediatric_newborn_examination_count = len(record.pediatric_newborn_examination_ids)

    @api.depends('pediatric_nicu_ids')
    def _compute_pediatric_nicu_count(self):
        for record in self:
            record.pediatric_nicu_count = len(record.pediatric_nicu_ids)

    @api.depends('pediatric_phototherapy_ids')
    def _compute_pediatric_phototherapy_count(self):
        for record in self:
            record.pediatric_phototherapy_count = len(record.pediatric_phototherapy_ids)

    @api.depends('pediatric_surgery_clinic_ids')
    def _compute_pediatric_surgery_clinic_count(self):
        for record in self:
            record.pediatric_surgery_clinic_count = len(record.pediatric_surgery_clinic_ids)

    @api.depends('pediatric_surgery_ids')
    def _compute_pediatric_surgery_count(self):
        for record in self:
            record.pediatric_surgery_count = len(record.pediatric_surgery_ids)

    @api.depends('pediatric_ward_admission_ids')
    def _compute_pediatric_ward_admission_count(self):
        for record in self:
            record.pediatric_ward_admission_count = len(record.pediatric_ward_admission_ids)

    @api.depends('rhs_gynochological_clinic_visit_ids')
    def _compute_rhs_gynochological_clinic_visit_count(self):
        for record in self:
            record.rhs_gynochological_clinic_visit_count = len(record.rhs_gynochological_clinic_visit_ids)

    @api.depends('rhs_awareness_ids')
    def _compute_rhs_awareness_count(self):
        for record in self:
            record.rhs_awareness_count = len(record.rhs_awareness_ids)

    @api.depends('rhs_anc_visit_ids')
    def _compute_rhs_anc_visit_count(self):
        for record in self:
            record.rhs_anc_visit_count = len(record.rhs_anc_visit_ids)

    @api.depends('rhs_anc_ids')
    def _compute_rhs_anc_count(self):
        for record in self:
            record.rhs_anc_count = len(record.rhs_anc_ids)

    @api.depends('rhs_delivery_ids')
    def _compute_rhs_delivery_count(self):
        for record in self:
            record.rhs_delivery_count = len(record.rhs_delivery_ids)

    @api.depends('rhs_edc_ids')
    def _compute_rhs_edc_count(self):
        for record in self:
            record.rhs_edc_count = len(record.rhs_edc_ids)

    @api.depends('rhs_fp_ids')
    def _compute_rhs_fp_count(self):
        for record in self:
            record.rhs_fp_count = len(record.rhs_fp_ids)

    @api.depends('rhs_hospitalization_monitoring_ids')
    def _compute_rhs_hospitalization_monitoring_count(self):
        for record in self:
            record.rhs_hospitalization_monitoring_count = len(record.rhs_hospitalization_monitoring_ids)

    @api.depends('rhs_hospitalization_ids')
    def _compute_rhs_hospitalization_count(self):
        for record in self:
            record.rhs_hospitalization_count = len(record.rhs_hospitalization_ids)

    @api.depends('rhs_infertility_treatment_ids')
    def _compute_rhs_infertility_treatment_count(self):
        for record in self:
            record.rhs_infertility_treatment_count = len(record.rhs_infertility_treatment_ids)

    @api.depends('rhs_pnc_visit_ids')
    def _compute_rhs_pnc_visit_count(self):
        for record in self:
            record.rhs_pnc_visit_count = len(record.rhs_pnc_visit_ids)

    @api.depends('rhs_pnc_ids')
    def _compute_rhs_pnc_count(self):
        for record in self:
            record.rhs_pnc_count = len(record.rhs_pnc_ids)

    @api.depends('rhs_surgery_ids')
    def _compute_rhs_surgery_count(self):
        for record in self:
            record.rhs_surgery_count = len(record.rhs_surgery_ids)

    @api.depends('general_clinic_visit_ids')
    def _compute_general_clinic_visit_count(self):
        for record in self:
            record.general_clinic_visit_count = len(record.general_clinic_visit_ids)


    def _action_get_service_records(self, res_model):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Patient Service',
            'view_mode': 'tree,form',
            'res_model': res_model,
            'domain': [('patient_id', '=', self.id)],
            'context': {'default_patient_id': self.id}
        }

    def action_get_em_hms_chw_individual_session(self):
        return self._action_get_service_records('em.hms.chw.individual.session')

    def action_get_em_hms_dial_kidney_history(self):
        return self._action_get_service_records('em.hms.dial.kidney.history')

    def action_get_em_hms_dial_lithotripsy(self):
        return self._action_get_service_records('em.hms.dial.lithotripsy')

    def action_get_em_hms_dial_nephrology(self):
        return self._action_get_service_records('em.hms.dial.nephrology')

    def action_get_em_hms_dial_prescription(self):
        return self._action_get_service_records('em.hms.dial.prescription')

    def action_get_em_hms_dial_urology(self):
        return self._action_get_service_records('em.hms.dial.urology')

    def action_get_em_hms_dial_visit(self):
        return self._action_get_service_records('em.hms.dial.visit')

    def action_get_em_hms_mh_gap(self):
        return self._action_get_service_records('em.hms.mh.gap')

    def action_get_em_hms_mh_pmplus(self):
        return self._action_get_service_records('em.hms.mh.pmplus')

    def action_get_em_hms_mh_referral(self):
        return self._action_get_service_records('em.hms.mh.referral')

    def action_get_em_hms_necessity_giving(self):
        return self._action_get_service_records('em.hms.necessity.giving')

    def action_get_em_hms_nutrition_screening_child(self):
        return self._action_get_service_records('em.hms.nutrition.screening.child')

    def action_get_em_hms_nutrition_screening_woman(self):
        return self._action_get_service_records('em.hms.nutrition.screening.woman')

    def action_get_em_hms_nutrition_stabilization_center(self):
        return self._action_get_service_records('em.hms.nutrition.stabilization.center')

    def action_get_em_hms_patient_admission_surgery(self):
        return self._action_get_service_records('em.hms.patient.admission.surgery')

    def action_get_em_hms_patient_admission_visit(self):
        return self._action_get_service_records('em.hms.patient.admission.visit')

    def action_get_em_hms_patient_admission(self):
        return self._action_get_service_records('em.hms.patient.admission')

    def action_get_em_hms_pediatric_clinic(self):
        return self._action_get_service_records('em.hms.pediatric.clinic')

    def action_get_em_hms_pediatric_icu(self):
        return self._action_get_service_records('em.hms.pediatric.icu')

    def action_get_em_hms_pediatric_incubator_admission(self):
        return self._action_get_service_records('em.hms.pediatric.incubator.admission')

    def action_get_em_hms_pediatric_newborn_examination(self):
        return self._action_get_service_records('em.hms.pediatric.newborn.examination')

    def action_get_em_hms_pediatric_nicu(self):
        return self._action_get_service_records('em.hms.pediatric.nicu')

    def action_get_em_hms_pediatric_phototherapy(self):
        return self._action_get_service_records('em.hms.pediatric.phototherapy')

    def action_get_em_hms_pediatric_surgery_clinic(self):
        return self._action_get_service_records('em.hms.pediatric.surgery.clinic')

    def action_get_em_hms_pediatric_surgery(self):
        return self._action_get_service_records('em.hms.pediatric.surgery')

    def action_get_em_hms_pediatric_ward_admission(self):
        return self._action_get_service_records('em.hms.pediatric.ward.admission')

    def action_get_em_hms_rhs_gynochological_clinic_visit(self):
        return self._action_get_service_records('em.hms.rhs.gynochological.clinic.visit')

    def action_get_em_hms_rhs_awareness(self):
        return self._action_get_service_records('em.hms.rhs.awareness')

    def action_get_em_hms_rhs_anc_visit(self):
        return self._action_get_service_records('em.hms.rhs.anc.visit')

    def action_get_em_hms_rhs_anc(self):
        return self._action_get_service_records('em.hms.rhs.anc')

    def action_get_em_hms_rhs_delivery(self):
        return self._action_get_service_records('em.hms.rhs.delivery')

    def action_get_em_hms_rhs_edc(self):
        return self._action_get_service_records('em.hms.rhs.edc')

    def action_get_em_hms_rhs_fp(self):
        return self._action_get_service_records('em.hms.rhs.fp')

    def action_get_em_hms_rhs_hospitalization_monitoring(self):
        return self._action_get_service_records('em.hms.rhs.hospitalization.monitoring')

    def action_get_em_hms_rhs_hospitalization(self):
        return self._action_get_service_records('em.hms.rhs.hospitalization')

    def action_get_em_hms_rhs_infertility_treatment(self):
        return self._action_get_service_records('em.hms.rhs.infertility.treatment')

    def action_get_em_hms_rhs_pnc_visit(self):
        return self._action_get_service_records('em.hms.rhs.pnc.visit')

    def action_get_em_hms_rhs_pnc(self):
        return self._action_get_service_records('em.hms.rhs.pnc')

    def action_get_em_hms_rhs_surgery(self):
        return self._action_get_service_records('em.hms.rhs.surgery')

    def action_get_em_hms_general_clinic_visit(self):
        return self._action_get_service_records('em.hms.general.clinic.visit')
    