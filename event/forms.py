
from django import forms
from .models import Service

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone  # Import timezone
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'location']
        widgets = {
            'date': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control'
                },
                format='%Y-%m-%dT%H:%M'
            ),
        }

    def clean_date(self):
        date = self.cleaned_data['date']
        if date < timezone.now():  # Use timezone.now() instead of datetime.now()
            raise ValidationError("The date cannot be in the past!")
        return date


from django import forms
from .models import Booking

from django import forms
from .models import Booking, Service


# forms.py
from django import forms
from .models import Booking, Service

class BookingForm(forms.ModelForm):
    event_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True
    )
    event_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),
        required=True
    )

    class Meta:
        model = Booking
        fields = [
            'service_name',
            'name',
            'email',
            'phone',
            'event_date',
            'event_time',
            'additional_services',
            'message'
        ]
        widgets = {
            'service_name': forms.TextInput(attrs={'readonly': 'readonly'}),
            'additional_services': forms.CheckboxSelectMultiple(),
            'message': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'additional_services': 'Select Additional Services',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply Tailwind classes to all fields except checkboxes
        for field_name, field in self.fields.items():
            if field_name != 'additional_services':
                field.widget.attrs.update({
                    'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500'
                })