from django import forms
from .models import Subscription

class CreateSubscriptionForm(forms.ModelForm):

    class Meta:
        model = Subscription
        fields = ['user', 'reference']
