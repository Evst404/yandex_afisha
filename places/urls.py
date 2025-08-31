from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # главная страница с картой
    path('places/<int:place_id>/', views.place_json, name='place_json'),  # JSON сразу по id
]