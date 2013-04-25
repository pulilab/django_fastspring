from django.contrib import admin
from .models import Subscription


class SubscriptionAdmin(admin.ModelAdmin):
    list_display =('reference', 'user', 'productName', 'quantity', 'nextPeriodDate', 'is_active')
    #date_hierarchy = 'created'
    list_filter  = ('productName', )
    search_fields = ('reference', 'user', 'productName', )
    
    def is_active(self, obj):
        return obj.is_active
    is_active.allow_tags = True

    
admin.site.register(Subscription, SubscriptionAdmin)
