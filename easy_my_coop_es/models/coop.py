from odoo import fields, models


class SubscriptionRequest(models.Model):
    _inherit = 'subscription.request'

    vat = fields.Char(
        string='Tax ID',
        help="The Tax Identification Number. Complete it if the contact is subjected to government taxes. Used in some legal statements."
    )

    def get_partner_vals(self):
        vals = super(SubscriptionRequest, self).get_partner_vals()
        vals['vat'] = self.vat
        return vals
