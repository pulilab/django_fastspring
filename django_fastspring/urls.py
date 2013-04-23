from django.conf.urls import patterns, url
from .views import ActivateSubscription

urlpatterns = patterns('',
    url(r'^subscriptions/activated/$', ActivateSubscription.as_view(), name='fastspring_subscription_activate'),
)