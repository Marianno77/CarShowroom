import datetime

from django.contrib import messages
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, DetailView

from CarShowroom.forms import CalendarsForm, ContactForm
from CarShowroom.models import Car, Equipment, Count, CarImage, Calendars


# Create your views here.

class Main(ListView):
    model = Car
    template_name = 'CarShowroom/main.html'
    context_object_name = 'cars'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        count_people, created = Count.objects.get_or_create(id=1)
        count_people.count += 1
        count_people.save()
        context['count_visit'] = count_people.count
        context['count_reserve'] = Count.objects.get(id=2).count
        context['form'] = ContactForm()

        return context

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            send_mail(
                subject=subject,
                message=f"Od: {name} <{email}>\n\n{message}",
                from_email='noreply@twojastrona.pl',
                recipient_list=['odbiorca@twojastrona.pl'],
            )
            return redirect('main')
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)


class CarDetail(DetailView):
    model = Car
    template_name = 'CarShowroom/car.html'
    context_object_name = 'car'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = CarImage.objects.filter(car=self.object)[:5]
        context['equipments'] = Equipment.objects.all()
        context['form'] = CalendarsForm(initial={'car': self.object})

        return context


    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CalendarsForm(request.POST)
        if form.is_valid():
            form.save()
            count_reserve, created = Count.objects.get_or_create(id=2)
            count_reserve.count += 1
            count_reserve.save()
            messages.success(request, "Rezerwacja została zapisana pomyślnie.")
            return redirect(self.object.get_absolute_url())
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)

def get_available_times(request):
    car_id = request.GET.get('car_id')
    date_str = request.GET.get('date')

    if not car_id or not date_str:
        return JsonResponse({'error': 'car_id and date are required'}, status=400)

    try:
        car = Car.objects.get(pk=car_id)
        date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()

        start = datetime.datetime.combine(date, datetime.time(8, 0))
        end = datetime.datetime.combine(date, datetime.time(16, 0))
        step = datetime.timedelta(minutes=30)
        current = start

        busy_times = Calendars.objects.filter(car=car, date=date).values_list('time', flat=True)
        available_times = []

        while current <= end:
            if current.time() not in busy_times:
                available_times.append(current.strftime('%H:%M'))
            current += step

        return JsonResponse({'times': available_times})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
