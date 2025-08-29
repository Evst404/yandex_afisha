import json
import os
import requests
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.conf import settings
from places.models import Place, PlaceImage

class Command(BaseCommand):
    help = 'Импортирует места и картинки из JSON-файлов'

    def handle(self, *args, **options):
        folder = os.path.join(settings.BASE_DIR, 'static', 'places')
        files = [f for f in os.listdir(folder) if f.endswith('.json')]

        for filename in files:
            path = os.path.join(folder, filename)
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Создаём или обновляем место
            place, created = Place.objects.update_or_create(
                title=data['title'],
                defaults={
                    'description_short': data.get('description_short', ''),
                    'description_long': data.get('description_long', ''),
                    'coordinates': data.get('coordinates', {}),
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Создано место: {place.title}'))
            else:
                self.stdout.write(self.style.WARNING(f'Обновлено место: {place.title}'))

            # Импортируем картинки
            imgs = data.get('imgs', [])
            for order, url in enumerate(imgs):
                try:
                    resp = requests.get(url)
                    if resp.status_code == 200:
                        filename = os.path.basename(url)
                        img_obj = PlaceImage(place=place, order=order)
                        img_obj.image.save(filename, ContentFile(resp.content), save=True)
                        self.stdout.write(f'  Добавлена картинка: {filename}')
                    else:
                        self.stdout.write(f'  Ошибка загрузки: {url}')
                except Exception as e:
                    self.stdout.write(f'  Исключение при загрузке {url}: {e}')