import json
import os
from pathlib import Path

import requests
from requests.exceptions import RequestException

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import MultipleObjectsReturned

from places.models import Place, PlaceImage


class Command(BaseCommand):
    help = "Загружает место и картинки из JSON по URL или локальному пути"

    def add_arguments(self, parser):
        parser.add_argument("source", type=str, help="URL или путь к JSON")

    def handle(self, *args, **options):
        place_info = self.load_json(options["source"])
        place, created = self.update_or_create_place(place_info)

        msg = f"Создано место: {place.title}" if created else f"Обновлено место: {place.title}"
        self.stdout.write(self.style.SUCCESS(msg) if created else self.style.WARNING(msg))

        for order, img_url in enumerate(place_info.get("imgs", [])):
            filename = os.path.basename(img_url.split("?")[0]) or f"img_{order}.jpg"
            try:
                resp = requests.get(img_url, timeout=10)
                resp.raise_for_status()
                PlaceImage.objects.create(
                    place=place,
                    order=order,
                    image=ContentFile(resp.content, name=filename)
                )
                self.stdout.write(f"  Добавлена картинка: {filename}")
            except RequestException as e:
                self.stdout.write(self.style.ERROR(f"Ошибка запроса изображения {img_url}: {e}"))
            except OSError as e:
                self.stdout.write(self.style.ERROR(f"Ошибка сохранения изображения {filename}: {e}"))

    def load_json(self, source):
        if source.startswith(("http://", "https://")):
            try:
                resp = requests.get(source, timeout=10)
                resp.raise_for_status()
                return resp.json()
            except RequestException as e:
                raise CommandError(f"Ошибка запроса URL: {e}")
            except json.JSONDecodeError as e:
                raise CommandError(f"Ошибка декодирования JSON с URL: {e}")
        path = Path(source)
        if not path.exists():
            raise CommandError(f"Файл {path} не найден")
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, OSError) as e:
            raise CommandError(f"Ошибка открытия файла {path}: {e}")
        except json.JSONDecodeError:
            raise CommandError(f"Ошибка декодирования JSON в файле {path}")

    def update_or_create_place(self, info):
        defaults = {
            "short_description": info.get("description_short", ""),
            "long_description": info.get("description_long", ""),
            "coordinates": info.get("coordinates", {}),
        }
        try:
            return Place.objects.update_or_create(title=info["title"], defaults=defaults)
        except MultipleObjectsReturned:
            place = Place.objects.filter(title=info["title"]).first()
            Place.objects.filter(pk=place.pk).update(**defaults)
            return place, False
