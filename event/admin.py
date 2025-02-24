from django.contrib import admin
from event.models import Event,RSVP,Category


admin.site.register(Event)
admin.site.register(RSVP)
admin.site.register(Category)
