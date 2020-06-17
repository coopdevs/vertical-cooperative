from odoo import api, fields, models
from datetime import datetime


class SubscriptionUpgradeSponsee(models.TransientModel):
    _name = 'subscription.upgrade.sponsee'
    _description = 'Change a partner from sponsee to member'

    partner_id = fields.Many2one('res.partner',
                                 domain=[('coop_sponsee', '=', True)],
                                 required=True)
    share_product_id = fields.Many2one('product.product',
                                       string='Share type',
                                       domain=[('is_share', '=', True)],
                                       required=True)
    ordered_parts = fields.Integer(string='Number of Share',
                                   required=True,
                                   default=1)
    start_date = fields.Date(string='Start date',
                             required=True,
                             default=lambda self: self._get_default_start_date())

    @api.model
    def _get_default_start_date(self):
        return datetime.now().date()

    @api.multi
    def upgrade(self):
        self.ensure_one()
        SubscriptionRequest = self.env['subscription.request']
        vals_subscription = {
            'already_cooperator': True,
            'partner_id': self.partner_id.id,
            'ordered_parts': self.ordered_parts,
            'date': self.start_date,
            'source': 'manual',
            'share_product_id': self.share_product_id.id,
            'firstname': self.partner_id.firstname,
            'name': self.partner_id.name,
            'iban': self.partner_id.bank_ids[0].acc_number,
            'lastname': self.partner_id.lastname,
            'email': self.partner_id.email,
            'birthdate': self.partner_id.birthdate_date,
            'gender': self.partner_id.gender,
            'address': self.partner_id.street,
            'city': self.partner_id.city,
            'zip_code': self.partner_id.zip,
            'country_id': self.partner_id.country_id.id,
            'phone': self.partner_id.phone,
            'lang': self.partner_id.lang,
        }
        subscription = SubscriptionRequest.create(vals_subscription)
        subscription.validate_subscription_request()
        self.partner_id.sponsor_id = False
        return {
            'view_mode': 'form',
            'view_id': False,
            'view_type': 'form',
            'res_model': 'res.partner',
            'res_id': self.partner_id.id,
            'type': 'ir.actions.act_window',
        }
