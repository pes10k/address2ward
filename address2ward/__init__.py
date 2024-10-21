from dataclasses import dataclass
import json
from pathlib import Path
from typing import cast

from diskcache import Cache
from geopy.geocoders import Nominatim
import shapely
import shapely.wkt


@dataclass
class Coords:
    lat: float
    long: float


AddressCache = dict[str, tuple[float, float]]
WardId = int


@dataclass
class WardShape:
    ward: WardId
    shape: shapely.MultiPolygon


def get_ward_data() -> list[WardShape]:
    wards = []
    with open("./data/wards.json", "r") as json_data:
        for ward_number, ward_shape in json.load(json_data):
            ward = WardShape(int(ward_number), shapely.wkt.loads(ward_shape))
            wards.append(ward)
    return wards


def coords_for_address(address: str, cachedir: Path) -> Coords:
    cache = cast(AddressCache, Cache(cachedir))
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
