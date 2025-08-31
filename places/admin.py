from django import forms
from django.contrib import admin
from django.utils.html import format_html
from adminsortable2.admin import SortableInlineAdminMixin, SortableAdminBase
from ckeditor.widgets import CKEditorWidget

from .models import Place, PlaceImage


class PlaceForm(forms.ModelForm):
    description_long = forms.CharField(widget=CKEditorWidget(), required=False)
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


class PlaceImageInline(SortableInlineAdminMixin, admin.TabularInline):
    model = PlaceImage
    extra = 0
    fields = ("image", "preview")  # убрали поле order
    readonly_fields = ("preview",)

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height:200px;"/>', obj.image.url)
        return "Нет изображения"
    preview.short_description = "Превью"


@admin.register(Place)
class PlaceAdmin(SortableAdminBase, admin.ModelAdmin):
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
    list_display = ("place", "preview")
    list_filter = ("place",)
    readonly_fields = ("preview",)

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height:100px;"/>', obj.image.url)
        return "Нет изображения"
    preview.short_description = "Превью"