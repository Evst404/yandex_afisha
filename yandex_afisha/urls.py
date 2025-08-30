from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from places import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),  # теперь главная страница через view
    path('places/<int:place_id>/json/', views.place_json, name='place_json'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)