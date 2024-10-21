from dataclasses import dataclass
import json
from pathlib import Path
from typing import cast

from diskcache import Cache
from geopy.geocoders import Nominatim
from shapely import MultiPolygon
import shapely.wkt


@dataclass
class Coords:
    lat: float
    long: float


WardId = int


@dataclass
class WardShape:
    ward: WardId
    shape: MultiPolygon


def get_ward_data() -> list[WardShape]:
    wards = []
    with open("./data/wards.json", "r", encoding="utf8") as json_data:
        for ward_number, ward_shape_text in json.load(json_data):
            ward_number = int(ward_number)
            ward_shape = cast(MultiPolygon, shapely.wkt.loads(ward_shape_text))
            ward = WardShape(ward_number, ward_shape)
            wards.append(ward)
    return wards


def coords_for_address(address: str, cachedir: Path) -> Coords:
    cache = Cache(cachedir)
    if address in cache:
        return Coords(*cache[address])

    geolocator = Nominatim(user_agent="address2ward: map chicago addresses to chicago wards")
    location = geolocator.geocode(address, timeout=30)
    coords = Coords(location.latitude, location.longitude)

    cache[address] = (coords.lat, coords.long)
    cache.close()
    return coords


def ward_for_address(address: str, cachedir: Path) -> WardId | None:
    coords = coords_for_address(address, cachedir)
    point = shapely.Point(coords.long, coords.lat)
    ward_data = get_ward_data()
    for ward in ward_data:
        if ward.shape.contains(point):
            return ward.ward
    return None
