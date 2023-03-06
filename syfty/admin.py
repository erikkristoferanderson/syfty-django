from django.contrib import admin

from .models import Syft, Subscription

admin.site.register(Syft)
admin.site.register(Subscription)
