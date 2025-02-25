from django.urls import path
from event.views import create_event, event_list, create_category,update_event,delete_event,organizer_dashboard,participant_dashboard,rsvp_event

urlpatterns = [
    path('create-event/',create_event, name='create-event'),
    path('events/',event_list, name='event-list'),    
    path('create-category/',create_category, name='create-category'),
    path('update-event/<int:id>/', update_event, name='update-event'),
    path('delete-event/<int:id>/', delete_event,name='delete-event'),
    path('organizer-dashboard/', organizer_dashboard, name='organizer-dashboard'), 
    path('event/<int:event_id>/rsvp/', rsvp_event, name='rsvp-event'),
]
