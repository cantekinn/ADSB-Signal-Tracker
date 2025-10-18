# utils.py
import math
from datetime import datetime


def haversine_km(lat1, lon1, lat2, lon2):
    """İki nokta arası mesafe hesapla (Haversine formülü)"""
    if lat1 == lat2 and lon1 == lon2:
        return 0.0

    R = 6371.0  # Dünya yarıçapı (km)
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    lat1_r = math.radians(lat1)
    lat2_r = math.radians(lat2)

    a = (math.sin(dlat / 2) ** 2 +
         math.cos(lat1_r) * math.cos(lat2_r) * math.sin(dlon / 2) ** 2)

    return 2 * R * math.asin(math.sqrt(min(1.0, a)))


def calculate_bearing(lat1, lon1, lat2, lon2):
    """İki nokta arası bearing hesapla (0-360 derece, kuzey=0)"""
    if lat1 == lat2 and lon1 == lon2:
        return None

    lat1_r = math.radians(lat1)
    lat2_r = math.radians(lat2)
    dlon_r = math.radians(lon2 - lon1)

    y = math.sin(dlon_r) * math.cos(lat2_r)
    x = (math.cos(lat1_r) * math.sin(lat2_r) -
         math.sin(lat1_r) * math.cos(lat2_r) * math.cos(dlon_r))

    bearing = math.degrees(math.atan2(y, x))
    return (bearing + 360) % 360


def normalize_angle(angle):
    """Açıyı 0-360 arası normalize et"""
    if angle is None:
        return None
    return (angle % 360 + 360) % 360


def angle_difference(a1, a2):
    """İki açı arası kısa mesafeyi hesapla (-180 ile 180 arası)"""
    if a1 is None or a2 is None:
        return 0

    a1, a2 = normalize_angle(a1), normalize_angle(a2)
    diff = a2 - a1

    if diff > 180:
        diff -= 360
    elif diff < -180:
        diff += 360

    return diff


def smooth_angle(current, target, alpha):
    """Açı yumuşatma (exponential smoothing)

    Args:
        current: Mevcut açı
        target: Hedef açı
        alpha: Yumuşatma faktörü (0-1, 1 = hedefi tamamen al)

    Returns:
        Yumuşatılmış açı
    """
    # Circular import'u önlemek için burada import ediyoruz
    import config

    if current is None:
        return target
    if target is None:
        return current

    diff = angle_difference(current, target)

    # Çok küçük değişimleri yoksay
    if abs(diff) < config.MIN_TRACK_CHANGE:
        return current

    return normalize_angle(current + diff * alpha)


def implied_speed_kts(lat1, lon1, ts1, lat2, lon2, ts2):
    """İki pozisyon arası ortalama hız hesapla (knot)

    Args:
        lat1, lon1: İlk pozisyon
        ts1: İlk pozisyon zamanı (unix timestamp)
        lat2, lon2: İkinci pozisyon
        ts2: İkinci pozisyon zamanı (unix timestamp)

    Returns:
        Hız (knot cinsinden), hata varsa inf
    """
    dt = ts2 - ts1
    if dt <= 0:
        return float('inf')

    dist_km = haversine_km(lat1, lon1, lat2, lon2)
    kmh = (dist_km * 3600.0) / dt  # km/saat
    return kmh / 1.852  # knot'a çevir


def debug_log(message, level="INFO"):
    """Debug logging (config.DEBUG_MODE aktifse)

    Args:
        message: Log mesajı
        level: Log seviyesi (INFO, WARNING, ERROR)
    """
    # Circular import'u önlemek için burada import
    import config

    if config.DEBUG_MODE:
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        print(f"[{timestamp}] {level}: {message}")


def format_altitude(altitude):
    """Yükseklik formatla (ft veya m)

    Args:
        altitude: Yükseklik değeri

    Returns:
        Formatlanmış string
    """
    if altitude is None:
        return "N/A"

    if altitude == "ground":
        return "Ground"

    try:
        alt = int(altitude)
        return f"{alt:,} ft"
    except (ValueError, TypeError):
        return "N/A"


def format_speed(speed):
    """Hız formatla (knot)

    Args:
        speed: Hız değeri (knot)

    Returns:
        Formatlanmış string
    """
    if speed is None:
        return "N/A"

    try:
        spd = int(speed)
        return f"{spd} kts"
    except (ValueError, TypeError):
        return "N/A"


def format_heading(heading):
    """Heading formatla (derece + yön)

    Args:
        heading: Heading değeri (0-360)

    Returns:
        Formatlanmış string (örn: "045° NE")
    """
    if heading is None:
        return "N/A"

    try:
        hdg = int(heading)

        # Yön belirleme
        directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
        index = int((hdg + 22.5) / 45) % 8
        direction = directions[index]

        return f"{hdg:03d}° {direction}"
    except (ValueError, TypeError):
        return "N/A"


def calculate_distance_nm(lat1, lon1, lat2, lon2):
    """İki nokta arası mesafe (nautical mile)

    Args:
        lat1, lon1: İlk pozisyon
        lat2, lon2: İkinci pozisyon

    Returns:
        Mesafe (nautical mile)
    """
    km = haversine_km(lat1, lon1, lat2, lon2)
    return km * 0.539957  # km -> nautical mile


def is_valid_position(lat, lon):
    """Pozisyon geçerli mi kontrol et

    Args:
        lat: Enlem
        lon: Boylam

    Returns:
        True/False
    """
    if lat is None or lon is None:
        return False

    try:
        lat = float(lat)
        lon = float(lon)
        return -90 <= lat <= 90 and -180 <= lon <= 180
    except (ValueError, TypeError):
        return False


def clamp(value, min_value, max_value):
    """Değeri min-max arasında sınırla

    Args:
        value: Değer
        min_value: Minimum
        max_value: Maximum

    Returns:
        Sınırlanmış değer
    """
    return max(min_value, min(value, max_value))


def calculate_eta(distance_nm, speed_kts):
    """Tahmini varış süresi hesapla

    Args:
        distance_nm: Mesafe (nautical mile)
        speed_kts: Hız (knot)

    Returns:
        Süre (saat), hata varsa None
    """
    if speed_kts is None or speed_kts <= 0:
        return None

    try:
        hours = distance_nm / speed_kts
        return hours
    except (ZeroDivisionError, TypeError):
        return None


def format_duration(hours):
    """Süreyi formatla (saat:dakika)

    Args:
        hours: Saat cinsinden süre

    Returns:
        Formatlanmış string
    """
    if hours is None:
        return "N/A"

    try:
        h = int(hours)
        m = int((hours - h) * 60)
        return f"{h}h {m}m"
    except (ValueError, TypeError):
        return "N/A"