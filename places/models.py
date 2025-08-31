from django.db import models
from ckeditor.fields import RichTextField

class Place(models.Model):
    title = models.CharField("Название места", max_length=300)
    description_short = models.TextField("Краткое описание", blank=True)
    description_long = RichTextField("Длинное описание", blank=True)
    coordinates = models.JSONField("Координаты", default=dict)

    def __str__(self):
        return self.title

    def latitude(self):
        return float(self.coordinates.get("lat", 0))

    def longitude(self):
        return float(self.coordinates.get("lng", 0))


class PlaceImage(models.Model):
    place = models.ForeignKey(Place, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField("Картинка", upload_to="place_images/")
    order = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.place.title} - {self.order}"