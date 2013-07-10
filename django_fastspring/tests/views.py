import datetime
from mock import MagicMock

from django.contrib.auth.models import User
from django.test import TestCase, Client

from django_fastspring import fastspring

class ActivateSubscriptionTest(TestCase):

    urls = 'django_fastspring.urls'

    def setUp(self):
        self.user = User.objects.create_user(username='me@example.com', email='me@example.com', password='mypass')
        self.client = Client(enforce_csrf_checks=True)

    def test_create_subscription(self):
        mock_subscription = type('Subscription', (object,), {
            'nextPeriodDate': datetime.date.today(),
            'status': 'active',
            'productName': "TestProduct",
            'quantity': 5,
            'is_test': False
        })()
        fastspring.getSubscription = MagicMock(name='getSubscription', return_value=mock_subscription)

        resp = self.client.post('/subscriptions/activated/', data={'reference': 'VID123456789', 'user': self.user.pk})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content, 'OK')
        self.assertEqual(self.user.subscription_set.filter(status='active').count(), 1)
