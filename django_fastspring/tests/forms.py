import datetime
from mock import MagicMock

from django.contrib.auth.models import User
from django.test import TestCase

from django_fastspring import fastspring
from ..forms import CreateSubscriptionForm

class CreateSubscriptionFormTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='me@example.com', email='me@example.com', password='mypass')

    def test_create_subscription(self):
        mock_subscription = type('Subscription', (object,), {
            'nextPeriodDate': datetime.date.today(),
            'status': 'active',
            'productName': "TestProduct",
            'quantity': 5,
            'is_test': False
        })()

        form = CreateSubscriptionForm(data={'reference': 'VID123456789', 'user': self.user.pk})

        self.assertTrue(form.is_valid())
        fastspring.getSubscription = MagicMock(name='getSubscription', return_value=mock_subscription)
        subscription = form.save()
