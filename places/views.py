from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.urls import reverse
from .models import Place


def index(request):
    places = Place.objects.all().prefetch_related('images')
    features = []

    for place in places:
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [place.longitude(), place.latitude()],
            },
            "properties": {
                "title": place.title,
                "placeId": f"place_{place.id}",
                "detailsUrl": reverse("place_detail", args=[place.id]),
            }
        })

    geojson = {
        "type": "FeatureCollection",
        "features": features
    }

    return render(request, "index.html", {"places_geojson": geojson})


def place_json(request, place_id):
    place = get_object_or_404(
        Place.objects.prefetch_related('images'),
        id=place_id
    )

    place_details = {
        "title": place.title,
        "short_description": place.short_description,
        "long_description": place.long_description,
        "imgs": [img.image.url for img in place.images.all()],
        "coordinates": {
            "lng": str(place.longitude()),
            "lat": str(place.latitude()),
        }
    }

    return JsonResponse(place_details, json_dumps_params={"ensure_ascii": False, "indent": 2})