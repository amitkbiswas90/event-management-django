from django.urls import path
from event.views import create_event, viewall_event, create_category,delete_participants,update_event,delete_event,organizer_dashboard, create_participants

urlpatterns = [
    path('create-event/',create_event, name='create-event'),
    path('viewall-event/',viewall_event, name='viewall-event'),
    path('create-category/',create_category, name='create-category'),
    path('delete-participants/',delete_participants, name= 'delete-participants'),
    path('update-event/<int:id>/', update_event, name='update-event'),
    path('delete-event/<int:id>/', delete_event,name='delete-event'),
    path('organizer-dashboard/', organizer_dashboard, name='organizer-dashboard'), 
    path('create-participant/',create_participants, name='create-participant'), 
]
