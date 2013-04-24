from django.http import HttpResponse
from django.views.generic.edit import CreateView

from .models import Subscription
from .forms import CreateSubscriptionForm


class ActivateSubscription(CreateView):
    model = Subscription
    form_class = CreateSubscriptionForm

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponse('OK')
