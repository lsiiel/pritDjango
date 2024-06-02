from django.urls import path
from .views import process_image, upload_form, mainPage, calculate_area

urlpatterns = [
    path('process-image/', process_image, name='process_image'),
    path('main/', mainPage, name='mainPage'),
    path('upload/', upload_form, name='upload_form'),
    path('calculate-area/', calculate_area, name='calculate_area'),
]
