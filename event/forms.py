# forms.py
from django import forms
from event.models import Event, Category

class StyleMixin:
    """Tailwind CSS form styling mixin"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        base_input_style = "w-full px-4 py-2 border rounded-lg focus:ring-2 focus:outline-none transition-all"
        
        for field_name, field in self.fields.items():
            # Common field styling
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    'class': f'{base_input_style} border-gray-300 focus:border-blue-500 focus:ring-blue-200'
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class': f'{base_input_style} border-gray-300 focus:border-blue-500 focus:ring-blue-200'
                })
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({
                    'class': f'{base_input_style} border-gray-300 focus:border-blue-500 focus:ring-blue-200 pr-10 bg-[url(\'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M19.5 8.25l-7.5 7.5-7.5-7.5" /></svg>\')] bg-no-repeat bg-[right:0.75rem_center] bg-[length:1.5em]'
                })
            elif isinstance(field.widget, forms.FileInput):
                field.widget.attrs.update({
                    'class': 'file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100'
                })
            elif isinstance(field.widget, forms.DateInput):
                field.widget.attrs.update({
                    'class': f'{base_input_style} border-gray-300 focus:border-blue-500 focus:ring-blue-200',
                    'type': 'date'
                })
            elif isinstance(field.widget, forms.TimeInput):
                field.widget.attrs.update({
                    'class': f'{base_input_style} border-gray-300 focus:border-blue-500 focus:ring-blue-200',
                    'type': 'time'
                })

class CategoryForm(StyleMixin, forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name', 'description']
        labels = {
            'category_name': 'Category Name',
            'description': 'Description'
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class EventForm(StyleMixin, forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'time', 'location', 'category', 'asset']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'name': 'Event Name',
            'description': 'Event Description',
            'date': 'Event Date',
            'time': 'Start Time',
            'location': 'Venue Location',
            'asset': 'Event Image',
            'category': 'Event Category',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].widget.attrs['min'] = '2024-01-01'