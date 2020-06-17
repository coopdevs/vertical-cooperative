#
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SubscriptionRequest(models.Model):
    _inherit = 'subscription.request'
    share_product_id = fields.Many2one(required=False)
    type = fields.Selection(selection_add=[('sponsorship', 'Sponsorship')])

    sponsor_id = fields.Many2one(
        'res.partner',
        string='Sponsor',
        domain=[
            ('member', '=', True),
        ]
    )

    @api.one
    def validate_subscription_request(self):
        try:
            invoice = super().validate_subscription_request()
        except UserError:
            if self.ordered_parts == 0 and self.type == 'sponsorship':
                pass
            else:
                raise
        else:
            return invoice

        self.partner_obj = self.env['res.partner']

        self._check_already_cooperator()

        if not self.partner:
            self.partner = self.create_coop_partner()
            self.partner_id = self.partner
        else:
            self.partner = self.partner[0]

        self.partner.cooperator = True

        self._create_company_contact()

        self.write({'state': 'done'})
        return True

    def _check_already_cooperator(self):
        if self.already_cooperator:
            raise UserError(
                _(
                    "The checkbox already cooperator is"
                    " checked please select a cooperator."
                )
            )
        elif self.is_company and self.company_register_number:
            domain = [
                (
                    "company_register_number",
                    "=",
                    self.company_register_number,
                )
            ]  # noqa
        elif not self.is_company and self.email:
            domain = [("email", "=", self.email)]

        if domain:
            self.partner = self.partner_obj.search(domain)

    def _create_company_contact(self):
        if self.is_company and not self.partner.has_representative():
            contact = False
            if self.email:
                domain = [('email', '=', self.email)]
                contact = self.partner_obj.search(domain)
                if contact:
                    contact.type = 'representative'
            if not contact:
                contact_vals = self.get_representative_vals()
                self.partner_obj.create(contact_vals)
            else:
                if len(contact) > 1:
                    raise UserError(_('There is two different persons with the'
                                      ' same national register number. Please'
                                      ' proceed to a merge before to continue')
                                    )
                if contact.parent_id and contact.parent_id.id != self.partner.id:
                    raise UserError(_('This contact person is already defined'
                                      ' for another company. Please select'
                                      ' another contact'))
                else:
                    contact.write({'parent_id': self.partner.id,
                                   'representative': True})

    def get_partner_company_vals(self):
        values = super().get_partner_company_vals()
        values['sponsor_id'] = self.sponsor_id.id
        return values

    def get_partner_vals(self):
        values = super().get_partner_vals()
        values['sponsor_id'] = self.sponsor_id.id
        return values
