import re

from django.db import models
from django.urls import reverse
from multiselectfield import MultiSelectField
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.

def convert_text(text):
    if not text:
        return ''

    text = str(text)

    text = re.sub(r'^###\s*(.*)', r'<h3>\1</h3>', text, flags=re.MULTILINE)
    text = re.sub(r'\n\n', '</p><p>', text)
    text = text.replace("\n", "<br>")

    if text[:3] == '<p>':
        return text
    else:
        return f'<p>{text}</p>'

class Car(models.Model):
    FUEL = [
        ('electric', 'elektryczny'),
        ('petrol', 'benzyna'),
        ('diesel', 'diesel')
    ]
    brand = models.CharField(default='Mercedes', max_length=200)
    model = models.CharField(max_length=200)
    text = models.TextField()
    fuel_type = MultiSelectField(choices=FUEL, blank=True)
    base_price = models.FloatField()
    object_file = models.FileField(upload_to='objects/')
    image = models.ImageField(upload_to='car-images/')



    def get_absolute_url(self):
        return reverse('car-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        if self.text:
            self.text = convert_text(str(self.text))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.brand} {self.model}"

class Equipment(models.Model):
    name = models.CharField(max_length=200)
    text = models.TextField()
    price = models.FloatField()
    image = models.ImageField(upload_to='eq-images/', blank=True, null=True)

    def __str__(self):
        return self.name

class Count(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    count = models.IntegerField(default=0)


    def __str__(self):
        return self.name

class CarImage(models.Model):
    car = models.ForeignKey(Car, related_name='images', on_delete=models.CASCADE)
    text = models.TextField()
    image = models.ImageField(upload_to='car-images/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.text:
            self.text = convert_text(str(self.text))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Zdjęcie dla {self.car.brand} {self.car.model} - {self.text[7:][:20]}"


class Calendars(models.Model):
    car = models.ForeignKey(Car, related_name='car_link', on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    phone_number = models.CharField(max_length=9)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.last_name} - {self.date} - {self.phone_number}'