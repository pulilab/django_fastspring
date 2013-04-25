import logging
logger = logging.getLogger('fastspring')

from django.http import HttpResponse
from django.views.generic.edit import CreateView

from .models import Subscription
from .forms import CreateSubscriptionForm


class ActivateSubscription(CreateView):
    model = Subscription
    form_class = CreateSubscriptionForm

    def form_valid(self, form):
        logger.debug('ActivateSubscription form_valid was called')
        self.object = form.save()
        return HttpResponse('OK')
