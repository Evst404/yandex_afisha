from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('places/<int:place_id>/json/', views.place_json, name='place_json'),
]