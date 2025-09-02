import json
import requests
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from django.core.files.base import ContentFile
from places.models import Place, PlaceImage
import os


class Command(BaseCommand):
    help = "Загружает место и картинки из JSON по URL или локальному пути"

    def add_arguments(self, parser):
        parser.add_argument("source", type=str, help="URL или путь к JSON")

    def handle(self, *args, **options):
        source = options["source"]

        # --- Загружаем JSON ---
        if source.startswith("http://") or source.startswith("https://"):
            try:
                response = requests.get(source)
                response.raise_for_status()
                data = response.json()
            except Exception as e:
                raise CommandError(f"Ошибка загрузки JSON из URL: {e}")
        else:
            path = Path(source)
            if not path.exists():
                raise CommandError(f"Файл {path} не найден")
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception as e:
                raise CommandError(f"Ошибка чтения JSON из файла: {e}")

        # --- Создаём или обновляем место ---
        place, created = Place.objects.update_or_create(
            title=data["title"],
            defaults={
                "description_short": data.get("description_short", ""),
                "description_long": data.get("description_long", ""),
                "coordinates": data.get("coordinates", {}),
            },
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f"Создано место: {place.title}"))
        else:
            self.stdout.write(self.style.WARNING(f"Обновлено место: {place.title}"))

        # --- Загружаем картинки ---
        for order, img_url in enumerate(data.get("imgs", [])):
            try:
                resp = requests.get(img_url)
                resp.raise_for_status()
                filename = os.path.basename(img_url.split("?")[0]) or f"img_{order}.jpg"
                img_obj = PlaceImage(place=place, order=order)
                img_obj.image.save(filename, ContentFile(resp.content), save=True)
                self.stdout.write(f"  Добавлена картинка: {filename}")
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"  Ошибка при загрузке {img_url}: {e}")
                )