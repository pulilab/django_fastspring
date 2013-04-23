from django.contrib.auth.models import User
from django.db import models
from model_utils.models import StatusModel
from model_utils.choices import Choices

import fastspring


class Subscription(StatusModel):
    PLANS = Choices('plan1', 'plan2', 'plan3')
    STATUS = Choices('active', 'inactive')

    user = models.ForeignKey(User)

    reference = models.CharField(max_length=255)
    nextPeriodDate = models.DateField(null=True)
    productName = models.CharField(max_length=255, choices=PLANS, blank=False, null=False)
    quantity = models.IntegerField()
    is_test = models.BooleanField(blank=True)
    is_active = property(lambda self: self.status == 'active')

    def save(self, *args, **kwargs):
        if not self.pk and self.user and self.reference:
            subscription = fastspring.getSubscription(self.reference)
            self.nextPeriodDate = subscription.nextPeriodDate
            self.status = subscription.status
            self.productName = subscription.productName
            self.quantity = subscription.quantity
            self.is_test = subscription.is_test
        return super(Subscription, self).save(*args, **kwargs)

    def updateFromFastspring(self, fields=['nextPeriodDate', 'status', 'productName', 'quantity', 'is_test']):
        """
        Update the DB entry with Fastspring data.

        @param fields: update only the specified fields, all if None
        """
        subscription = fastspring.getSubscription(self.reference)
        for f in fields:
            setattr(self, f, getattr(subscription, f, None))
        self.save()
        return self

    def updateOnFastspring(self):
        raise NotImplementedError

    def renew(self):
        raise NotImplementedError

    def cancel(self):
        raise NotImplementedError
