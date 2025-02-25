from django.urls import path
from core.views import home, event_view

urlpatterns = [
    path("",home, name="home"),
    path("event-view/",event_view, name="event-view")
]