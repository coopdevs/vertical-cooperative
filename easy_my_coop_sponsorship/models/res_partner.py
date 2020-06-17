from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    sponsee_ids = fields.One2many(
        'subscription.request',
        'sponsor_id',
        string='Sponsees',
        readonly=True
    )

    sponsor_id = fields.Many2one(
        'res.partner',
        string='Sponsor',
        domain=[
            ('member', '=', True),
        ]
    )
    coop_sponsee = fields.Boolean(string="Cooperator Sponsee",
                                  compute="_compute_coop_sponsee",
                                  store=True,
                                  readonly=True)

    @api.multi
    @api.depends("sponsor_id")
    @api.depends("subscription_request_ids.state")
    def _compute_coop_candidate(self):
        for partner in self:
            if partner.member:
                is_candidate = False
            else:
                sub_requests = partner.subscription_request_ids.filtered(
                    lambda record: (
                            record.state == 'done' and
                            not record.sponsor_id
                    )
                )
                is_candidate = bool(sub_requests)
            partner.coop_candidate = is_candidate

    @api.multi
    @api.depends("sponsor_id")
    def _compute_coop_sponsee(self):
        for partner in self:
            if partner.sponsor_id:
                partner.coop_sponsee = True
            else:
                partner.coop_sponsee = False