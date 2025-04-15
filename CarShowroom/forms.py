import datetime

from django import forms
from django.http import JsonResponse
from django.utils import timezone

from .models import Calendars

class CalendarsForm(forms.ModelForm):
    class Meta:
        model = Calendars
        fields = ['car','date','time','last_name','phone_number']

        labels = {
            'car': '',
            'date': 'data',
            'time': 'Godzina',
            'last_name': 'Nazwisko',
            'phone_number': 'Numer telefonu',
        }

        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.Select(),
        }

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')
        car = cleaned_data.get('car')
        phone_number = cleaned_data.get('phone_number')

        if date and date < timezone.now().date():
            raise forms.ValidationError("Data nie może być z przeszłości.")

        if time:
            open_time = datetime.time(8,0)
            close_time = datetime.time(16,0)

            if not (open_time <= time <= close_time):
                raise forms.ValidationError("Nasz salon jest otwarty od godziny 8 do 16.")

        if  car and date and time:
            if Calendars.objects.filter(car=car, date=date, time=time).exists():
                raise forms.ValidationError("Ta godzina jest już zajęta.")

        if len(phone_number) != 9:
            raise  forms.ValidationError("Podaj poprawny numer telefonu")


        return cleaned_data

class ContactForm(forms.Form):
    name = forms.CharField(label='Imię', max_length=100)
    email = forms.EmailField(label='Email')
    subject = forms.CharField(label='Temat', max_length=150)
    message = forms.CharField(label='Wiadomość', widget=forms.Textarea)
