from odoo import _, api, fields, models, exceptions, tools


class EmHmsMHAwareness(models.Model):
    _name = 'em.hms.mh.awareness'
    _description = 'Mental Health Group Awareness Session'
    _rec_name = 'session_date'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    session_date = fields.Date('Session Date', required=True, tracking=True)
    facilitator_name = fields.Char('Activity Facilitator Name', tracking=True)
    activity_name = fields.Selection([
        ('depression', 'Depression'),
        ('loss_sadness', 'Loss And Sadness'),
        ('psychological_pressure', 'Psychological Pressure'),
        ('post_traumatic_stress_disorder', 'Post-traumatic Stress Disorder')
    ], string='Activity Name', tracking=True)
    boys_count = fields.Integer('#Males < 18', tracking=True)
    men_count = fields.Integer('#Males >= 18', tracking=True)
    girls_count = fields.Integer('#Females < 18', tracking=True)
    women_count = fields.Integer('#Females >= 18', tracking=True)
    company_id = fields.Many2one('res.company', 'Medical Center', default = lambda self: self.env.company, required=True)
    