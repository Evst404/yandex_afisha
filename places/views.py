import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Place

# Главная страница с картой и GeoJSON
def index(request):
    places = Place.objects.all()
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
                "detailsUrl": f"/places/{place.id}/",  # <-- URL для fetch теперь без /json/
            }
        })

    geojson = {
        "type": "FeatureCollection",
        "features": features
    }

    return render(request, "index.html", {"places_geojson": json.dumps(geojson)})

# JSON детали одного места (для sidebar)
def place_json(request, place_id):
    place = get_object_or_404(Place, id=place_id)
    images = [img.image.url for img in place.images.all()]

    data = {
        "title": place.title,
        "description_short": place.description_short,
        "description_long": place.description_long,
        "imgs": images,
        "coordinates": {
            "lng": str(place.longitude()),
            "lat": str(place.latitude()),
        }
    }
    return JsonResponse(data)