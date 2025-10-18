# airports.py
"""
Türkiye ve çevre bölge havaalanları
"""

MAJOR_AIRPORTS = {
    # İstanbul
    'LTFM': {
        'name': 'İstanbul Havalimanı',
        'city': 'İstanbul',
        'lat': 41.2619,
        'lon': 28.7419,
        'elevation': 325,
        'type': 'international'
    },
    'LTFJ': {
        'name': 'Sabiha Gökçen Havalimanı',
        'city': 'İstanbul',
        'lat': 40.8986,
        'lon': 29.3092,
        'elevation': 312,
        'type': 'international'
    },

    # Ankara
    'LTAC': {
        'name': 'Esenboğa Havalimanı',
        'city': 'Ankara',
        'lat': 40.1281,
        'lon': 32.9951,
        'elevation': 3125,
        'type': 'international'
    },

    # İzmir
    'LTBJ': {
        'name': 'Adnan Menderes Havalimanı',
        'city': 'İzmir',
        'lat': 38.2924,
        'lon': 27.1570,
        'elevation': 412,
        'type': 'international'
    },

    # Antalya
    'LTAI': {
        'name': 'Antalya Havalimanı',
        'city': 'Antalya',
        'lat': 36.8987,
        'lon': 30.8005,
        'elevation': 177,
        'type': 'international'
    },

    # Diğer Büyük Havalimanları
    'LTCG': {
        'name': 'Milas-Bodrum Havalimanı',
        'city': 'Muğla',
        'lat': 37.2506,
        'lon': 27.6643,
        'elevation': 21,
        'type': 'international'
    },
    'LTFG': {
        'name': 'Dalaman Havalimanı',
        'city': 'Muğla',
        'lat': 36.7131,
        'lon': 28.7925,
        'elevation': 20,
        'type': 'international'
    },
    'LTCF': {
        'name': 'Gazipaşa-Alanya Havalimanı',
        'city': 'Antalya',
        'lat': 36.2992,
        'lon': 32.3006,
        'elevation': 86,
        'type': 'domestic'
    },
    'LTCK': {
        'name': 'Konya Havalimanı',
        'city': 'Konya',
        'lat': 37.9790,
        'lon': 32.5619,
        'elevation': 3392,
        'type': 'domestic'
    },
    'LTCE': {
        'name': 'Adana Şakirpaşa Havalimanı',
        'city': 'Adana',
        'lat': 36.9822,
        'lon': 35.2804,
        'elevation': 65,
        'type': 'international'
    },
    'LTCN': {
        'name': 'Hatay Havalimanı',
        'city': 'Hatay',
        'lat': 36.3628,
        'lon': 36.2824,
        'elevation': 246,
        'type': 'international'
    },
    'LTCL': {
        'name': 'Çukurova Havalimanı',
        'city': 'Adana',
        'lat': 36.9822,
        'lon': 35.2806,
        'elevation': 20,
        'type': 'domestic'
    },
    'LTAZ': {
        'name': 'Trabzon Havalimanı',
        'city': 'Trabzon',
        'lat': 40.9951,
        'lon': 39.7897,
        'elevation': 104,
        'type': 'international'
    },
}


def get_airports_geojson():
    """Havaalanlarını GeoJSON formatında döndür (Leaflet için)"""
    features = []

    for icao, airport in MAJOR_AIRPORTS.items():
        features.append({
            'type': 'Feature',
            'properties': {
                'icao': icao,
                'name': airport['name'],
                'city': airport['city'],
                'elevation': airport['elevation'],
                'type': airport['type']
            },
            'geometry': {
                'type': 'Point',
                'coordinates': [airport['lon'], airport['lat']]
            }
        })

    return {
        'type': 'FeatureCollection',
        'features': features
    }


def get_nearest_airport(lat, lon):
    """En yakın havaalanını bul"""
    from utils import haversine_km

    min_distance = float('inf')
    nearest = None

    for icao, airport in MAJOR_AIRPORTS.items():
        distance = haversine_km(lat, lon, airport['lat'], airport['lon'])
        if distance < min_distance:
            min_distance = distance
            nearest = {
                'icao': icao,
                **airport,
                'distance_km': distance
            }

    return nearest