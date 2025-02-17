from django import forms
from event.models import Event, Category, Participant


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name','description']
        labels = {
            'name': 'Category Name',
            'description': 'Description'
        }

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'time', 'location', 'category']
        widgets = {
            'date': forms.SelectDateWidget(years=range(2025, 2050)),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }
        labels = {
            'name': 'Event Name',
            'description': 'Event Description',
            'date': 'Event Date',
            'time': 'Start Time',
            'location': 'Venue Location'
        }
class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['name','email','event']
        labels = {
            'name': 'Full Name',
            'email': 'Email Address',
        }