from django.db import models
from ckeditor.fields import RichTextField
from django.core.exceptions import ValidationError


class Place(models.Model):
    title = models.CharField("Название места", max_length=300)
    short_description = models.TextField("Краткое описание", blank=True)
    long_description = RichTextField("Длинное описание", blank=True)
    coordinates = models.JSONField("Координаты") 

    def __str__(self):
        return self.title

    def latitude(self):
        return float(self.coordinates.get("lat"))

    def longitude(self):
        return float(self.coordinates.get("lng"))

    def clean(self):
        lat = self.coordinates.get("lat") if self.coordinates else None
        lng = self.coordinates.get("lng") if self.coordinates else None
        if lat is None or lng is None:
            raise ValidationError("Необходимо указать координаты (широту и долготу).")


class PlaceImage(models.Model):
    place = models.ForeignKey(
        Place,
        related_name="images",
        on_delete=models.CASCADE,
        verbose_name="Место"
    )
    image = models.ImageField("Картинка", upload_to="place_images/")
    order = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        ordering = ["order"]
        indexes = [
            models.Index(fields=["order"]),
        ]

    def __str__(self):
        return f"{self.place.title} - {self.order}"