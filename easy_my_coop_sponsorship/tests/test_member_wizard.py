from odoo.tests.common import TransactionCase
from datetime import datetime, timedelta


class TestMemberWizard(TransactionCase):

    def setUp(self, *args, **kwargs):
        result = super().setUp(*args, **kwargs)
        self.SubscriptionRequest = self.env['subscription.request']
        self.SponseeMemberWizard = self.env['subscription.upgrade.sponsee']
        sponsor_id = self.ref("easy_my_coop.res_partner_cooperator_1_demo")
        vals_subscription_sponsorship = {
            'already_cooperator': False,
            'name': 'Manuel Dublues Test',
            'email': 'manuel@demo-test.net',
            'ordered_parts': False,
            'address': 'schaerbeekstraat',
            'city': 'Brussels',
            'zip_code': '1111',
            'country_id': 20,
            'date': datetime.now()-timedelta(days=12),
            'company_id': 1,
            'source': 'manual',
            'share_product_id': False,
            'lang': 'en_US',
            'sponsor_id': sponsor_id,
            'type': 'sponsorship'
        }
        subscription_sponsorship = self.SubscriptionRequest.create(vals_subscription_sponsorship)
        subscription_sponsorship.validate_subscription_request()
        self.sponsee = subscription_sponsorship.partner_id

    def testSponseeToMemberWizardCreation(self):
        WizardSponsee = self.SponseeMemberWizard
        product_template = self.browse_ref('easy_my_coop.product_template_share_type_2_demo')
        wizardSponsee = WizardSponsee.create({
            'share_product_id': product_template.product_variant_id.id,
            'partner_id': self.sponsee.id
        })
        self.assertEqual(wizardSponsee.partner_id, self.sponsee)
        self.assertEqual(wizardSponsee.start_date, datetime.now().date())

    def testSponseeToMemberWizardUpgrade(self):
        WizardSponsee = self.SponseeMemberWizard
        product_template = self.browse_ref('easy_my_coop.product_template_share_type_2_demo')
        wizardSponsee = WizardSponsee.create({
            'share_product_id': product_template.product_variant_id.id,
            'partner_id': self.sponsee.id
        })
        wizardSponsee.upgrade()
        self.assertTrue(self.sponsee.coop_candidate)
        self.assertFalse(self.sponsee.coop_sponsee)
