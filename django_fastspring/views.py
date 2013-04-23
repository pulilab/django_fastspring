from django.views.generic.edit import CreateView

from .models import Subscription
from .forms import CreateSubscriptionForm


class ActivateSubscription(CreateView):
    model = Subscription
    form_class = CreateSubscriptionForm
    success_url = '/'