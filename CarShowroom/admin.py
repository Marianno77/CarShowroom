from django.contrib import admin

from CarShowroom.models import Car, Equipment, Count, CarImage, Calendars

# Register your models here.

admin.site.register(Car)
admin.site.register(Equipment)
admin.site.register(Count)
admin.site.register(CarImage)
admin.site.register(Calendars)
