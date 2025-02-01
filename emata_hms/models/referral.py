from odoo import _, api, fields, models, exceptions, tools


class EmHmsMHReferral(models.Model):
    _name = 'em.hms.referral'
    _description = 'Referral'
    _rec_name = 'referral_datetime'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'em.common.form']
    
    patient_id = fields.Many2one('res.partner', 'Patient Name', required=True, domain=[('is_patient','=',True)], tracking=True)
    referral_datetime = fields.Datetime('Referral Date/Time', required=True, tracking=True)
    type_of_referral = fields.Selection([
        ('cold', 'Cold'),
        ('emergency', 'Emergency')
    ], string='Type Of Referral', tracking=True)
    referrer_organizer_id = fields.Many2one('hr.employee', string='Facility That Organized The Referral')
    referred_to_entity = fields.Char('Facility To Which The Patient Was Referred', tracking=True)
    previous_cases = fields.Char('Previous Cases / Clinical Examination / Investigations', tracking=True)
    treatment_provided = fields.Char('Treatment Provided', tracking=True)
    reason_for_referral = fields.Selection([
        ('satisfied', 'Satisfied'),
        ('unsatisfied', 'Unsatisfied')
    ], string='Reason For Referral', tracking=True)
    diagnosis_id = fields.Many2one('em.hms.icd10', string='Diagnosis', tracking=True)
    services_required = fields.Selection([
        ('treatment', 'Treatment'),
        ('diagnostic_support', 'Diagnostic Support')
    ], string='Services Required', tracking=True)
    diagnostic_support_type = fields.Selection([
        ('rays', 'Rays'),
        ('laboratory', 'Laboratory')
    ], string='Type Of Diagnostic Support Required', tracking=True)
    radiology_type_required = fields.Selection([
        ('simple_echo', 'Simple Echo'),
        ('axial_layered', 'Axial Layered'),
        ('magnetic_resonance', 'Magnetic Resonance'),
        ('Mammography', 'Mammography'),
        ('vascular_shadow', 'Vascular Shadow'),
        ('panoramic_jaw', 'Panoramic Jaw')
    ], string='Type Of Radiology Required', tracking=True)
    treatment_type_required = fields.Selection([
        ('consultation', 'Consultation With A Specialist Doctor'),
        ('acceptance_facility', 'Acceptance of the facility'),
        ('devices', 'Devices')
    ], string='Type Of Treatment Required', tracking=True)
    facility_acceptance = fields.Selection([
        ('wing', 'Wing'),
        ('incubators', 'Incubators'),
        ('care', 'Care')
    ], string='Facility Acceptance', tracking=True)
    equipment_type_required = fields.Selection([
        ('kidney_washing', 'Kidney washing'),
        ('stone_fragmentation', 'Stone fragmentation'),
        ('physical_therapy', 'Physical therapy'),
        ('cardiac_catheterization', 'Cardiac catheterization'),
        ('digestive_endoscopy', 'Digestive endoscopy')
    ], string='Type Of Treatment Required', tracking=True)
    treatment_details = fields.Char('Details Of Treatment Required', tracking=True)
    speciality_required = fields.Selection([
        ('children', 'Children'),
        ('obstetrics_gynecology', 'Obstetrics and Gynecology'),
        ('internal_medicine', 'Internal Medicine'),
        ('ophthalmology', 'Ophthalmology'),
        ('general_surgery', 'General Surgery'),
        ('dermatology', 'Dermatology'),
        ('cardiology', 'Cardiology'),
        ('rheumatology', 'Rheumatology'),
        ('orthopedic_surgery', 'Orthopedic Surgery'),
        ('mental_health', 'Mental Health'),
        ('vaccination', 'Vaccination'),
        ('otorhinolaryngology', 'Otorhinolaryngology')
    ], string='Specialty Required', tracking=True)
    referral_coordination_datetime = fields.Datetime('Referral Coordination Date/Time', required=True, tracking=True)
    referring_id = fields.Many2one('hr.employee', string='Referring Physician')
    coordinating_contact_name = fields.Char('Name Of Coordinating Contact Person', tracking=True)
    transportation_information = fields.Selection([
        ('ambulance_center', 'Ambulance Center'),
        ('cold_referral_car', 'Cold Referral Car'),
        ('civil_defense_car', 'Civil Defense Car'),
        ('system_ambulance', 'System Ambulance'),
        ('other', 'Other')
    ], string='Transportation Information', tracking=True)
    referring_physician_id = fields.Many2one('hr.employee', string='Name Of Referring Physician')
    contact_person_id = fields.Many2one('hr.employee', string='Name Of Contact Person')
    referee_manager_id = fields.Many2one('hr.employee', string='Referee Line Manager')
    patient_companion_name = fields.Char('Name Of Patient''s Companion', tracking=True)
    company_id = fields.Many2one('res.company', 'Medical Center', default = lambda self: self.env.company)