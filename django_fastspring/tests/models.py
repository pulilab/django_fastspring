import datetime
from mock import MagicMock

from django.contrib.auth.models import User
from django.test import TestCase

from django_fastspring import fastspring
from ..models import Subscription


class SubscriptionManagerTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='myuser', email='me@example.com', password='mypass')

    def test_create(self):
        mock_subscription = type('Subscription', (object,), {
            'nextPeriodDate': datetime.date.today(),
            'status': 'active',
            'productName': "TestProduct",
            'quantity': 5,
            'is_test': False
        })()
        fastspring.getSubscription = MagicMock(name='getSubscription', return_value=mock_subscription)
        subscription = Subscription.objects.create(reference="VID130423-6618-64141S", user=self.user)
        self.assertEqual(fastspring.getSubscription.assert_called_once_with("VID130423-6618-64141S"), None)
        self.assertEqual(subscription.user, self.user)
        self.assertEqual(subscription.reference, "VID130423-6618-64141S")
        self.assertEqual(subscription.nextPeriodDate, datetime.date.today())
        self.assertEqual(subscription.status, Subscription.STATUS.active)
        self.assertEqual(subscription.productName, 'TestProduct')
        self.assertEqual(subscription.quantity, 5)
        self.assertEqual(subscription.is_test, False)
        self.assertEqual(subscription.is_active, True)


class SubscriptionTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='myuser', email='me@example.com', password='mypass')

    def test_update_all(self):
        today = datetime.date.today()
        mock_subscription = type('Subscription', (object,), {
            'nextPeriodDate': today,
            'status': 'active',
            'productName': "TestProduct",
            'quantity': 5,
            'is_test': False
        })()
        fastspring.getSubscription = MagicMock(name='getSubscription', return_value=mock_subscription)
        subscription = Subscription.objects.create(reference="VID130423-6618-64141S", user=self.user)

        fastspring.getSubscription.reset_mock()
        mock_subscription2 = type('Subscription', (object,), {
            'nextPeriodDate': today,
            'status': 'active',
            'productName': "TestProduct - 2",
            'quantity': 3,
            'is_test': True
        })()

        fastspring.getSubscription.return_value = mock_subscription2
        subscription = subscription.updateFromFastspring()

        self.assertEqual(fastspring.getSubscription.assert_called_once_with("VID130423-6618-64141S"), None)
        self.assertEqual(subscription.user, self.user)
        self.assertEqual(subscription.reference, "VID130423-6618-64141S")
        self.assertEqual(subscription.nextPeriodDate, today)
        self.assertEqual(subscription.status, Subscription.STATUS.active)
        self.assertEqual(subscription.productName, 'TestProduct - 2')
        self.assertEqual(subscription.quantity, 3)
        self.assertEqual(subscription.is_test, True)
        self.assertEqual(subscription.is_active, True)
