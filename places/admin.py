from django import forms
from django.contrib import admin
from .models import Place, PlaceImage


class PlaceForm(forms.ModelForm):
    latitude = forms.FloatField(label="Широта", required=False)
    longitude = forms.FloatField(label="Долгота", required=False)

    class Meta:
        model = Place
        fields = ("title", "description_short", "description_long", "latitude", "longitude")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.coordinates:
            self.fields["latitude"].initial = self.instance.coordinates.get("lat", 0)
            self.fields["longitude"].initial = self.instance.coordinates.get("lng", 0)

    def save(self, commit=True):
        instance = super().save(commit=False)
        lat = self.cleaned_data.get("latitude")
        lng = self.cleaned_data.get("longitude")
        instance.coordinates = {"lat": lat, "lng": lng}
        if commit:
            instance.save()
        return instance


class PlaceImageInline(admin.TabularInline):
    model = PlaceImage
    extra = 1
    fields = ('image', 'order')


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    form = PlaceForm
    list_display = ("title", "get_latitude", "get_longitude")
    inlines = [PlaceImageInline]

    def get_latitude(self, obj):
        return obj.coordinates.get("lat") if obj.coordinates else None
    get_latitude.short_description = "Широта"

    def get_longitude(self, obj):
        return obj.coordinates.get("lng") if obj.coordinates else None
    get_longitude.short_description = "Долгота"


@admin.register(PlaceImage)
class PlaceImageAdmin(admin.ModelAdmin):
    list_display = ('place', 'order', 'image')
    list_filter = ('place',)
    ordering = ('place', 'order')