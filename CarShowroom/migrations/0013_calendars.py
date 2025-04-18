# Generated by Django 5.1.7 on 2025-04-10 18:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CarShowroom', '0012_equipment_image_alter_carimage_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Calendars',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField()),
                ('time', models.TimeField()),
                ('phone_number', models.CharField(max_length=9)),
                ('last_name', models.CharField(blank=True, max_length=200, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='car_link', to='CarShowroom.car')),
            ],
        ),
    ]
