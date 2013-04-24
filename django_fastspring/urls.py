from django.conf.urls import patterns, url
from django.views.decorators.csrf import csrf_exempt
from .views import ActivateSubscription

urlpatterns = patterns('',
    url(r'^subscriptions/activated/$', csrf_exempt(ActivateSubscription.as_view()), name='fastspring_subscription_activate'),
)