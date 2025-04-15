from . import views
from django.urls import path

from CarShowroom.views import Main, CarDetail, get_available_times

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('',Main.as_view(),name='main'),
    path('car/<int:pk>',CarDetail.as_view(),name='car-detail'),
    path('ajax/get-times/', get_available_times, name='get_available_times'),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)