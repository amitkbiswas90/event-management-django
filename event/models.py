from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    category_name = models.CharField(max_length=250, unique=True)
    description = models.TextField(max_length=500)

    def __str__(self):
        return self.category_name

class Event(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(max_length=500)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='events')
    attendees = models.ManyToManyField(
        User, 
        through='RSVP',
        related_name='attended_events',
        blank=True
    )
    asset = models.ImageField(
        upload_to='event_asset',  
        blank=True, 
        null=True,
        default="event_asset/default-image.png"
    )

    def __str__(self):
        return self.name

class RSVP(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='rsvp'  # Explicitly set user's reverse relationship
    )
    event = models.ForeignKey(
        'Event', 
        on_delete=models.CASCADE,
        related_name='rsvps'  
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')

    def __str__(self):
        return f"{self.user.username} - {self.event.name}"