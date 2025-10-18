# config.py
from pathlib import Path

# =========================
# Proje Yolları
# =========================
PROJECT_ROOT = Path(__file__).resolve().parent
JSON_FILES_DIR = PROJECT_ROOT / "json_files"
DB_PATH = PROJECT_ROOT / "flight_history.db"

# =========================
# Özellik Bayrakları
# =========================
USE_SQLITE = False
DEBUG_MODE = True
USE_JSON_FILES = True  # JSON dosyalarından mı yoksa canlı dump1090'dan mı?

# =========================
# Dump1090 Ayarları (Canlı mod için)
# =========================
DUMP1090_URL = "http://localhost:8080/data/aircraft.json"
POLL_INTERVAL = 1.0  # Saniye

# =========================
# JSON Dosya Okuma Ayarları
# =========================
JSON_PLAYBACK_SPEED = 1.0  # 1.0 = gerçek zamanlı, 2.0 = 2x hızlı
JSON_LOOP = False  # ❌ DÖNGÜ KAPALI - Bitince dursun!
JSON_AUTO_EXIT = True  # ✅ JSON bitince programı kapat

# =========================
# Görüntüleme Filtreleri (GITHUB SUNUMU İÇİN OPTİMİZE!)
# =========================
MAX_DISPLAYED_AIRCRAFT = 300  # ✅ Aynı anda gösterilecek maksimum uçak

# Bölge Filtresi (Türkiye merkez - İstanbul/Ankara arası)
FOCUS_REGION = {
    'enabled': True,  # Bölge filtreleme aktif
    'center_lat': 40.0,  # İstanbul-Ankara ortası
    'center_lon': 29.0,  # Türkiye merkez
    'radius_km': 400  # ✅ 400km yarıçap (daha optimize - önceden 500km'di)
}

# Uçak İzleri (TIKLAMA İLE AÇILIR!)
AIRCRAFT_TRAIL = {
    'enabled': True,  # İzleri göster
    'max_points': 50,  # Maksimum iz noktası (son 50 pozisyon)
    'color': '#3b82f6',  # İz rengi (açık mavi - tema ile uyumlu)
    'weight': 3,  # İz kalınlığı
    'opacity': 0.7  # İz şeffaflığı
}

# =========================
# Pozisyon Filtreleme Parametreleri
# =========================
MAX_SPEED_KTS = 750.0  # Maksimum hız (knot) - ticari jetler için
MAX_JUMP_KM = 15.0  # Maksimum tek seferde sıçrama mesafesi
MIN_TIME_DIFF = 0.3  # Minimum zaman farkı (saniye)
POSITION_HISTORY_SIZE = 200  # ÇÖZÜM: Sınırlı ama yeterli! (eskiden 5'ti)

# Outlier detection (Anomali tespiti)
OUTLIER_DISTANCE_KM = 8.0  # Ortalamadan maksimum uzaklık
OUTLIER_SPEED_MULTIPLIER = 2.5  # Hız çarpanı (beklenen hızın 2.5 katı)

# Yumuşatma (Smoothing)
POSITION_SMOOTH_ALPHA = 0.2  # Pozisyon yumuşatma katsayısı (0-1)
TRACK_SMOOTH_ALPHA = 0.4  # Heading yumuşatma katsayısı (0-1)
MIN_TRACK_CHANGE = 5.0  # Minimum heading değişimi (derece)

# Heading hesaplama
USE_MOVEMENT_HEADING = True  # Gerçek hareket yönünü kullan
HEADING_CONFIDENCE_THRESHOLD = 0.1  # Minimum hareket mesafesi (km)

# =========================
# Global State (İstatistikler)
# =========================
_stats = {
    'total_updates': 0,
    'outliers_detected': 0,
    'position_corrections': 0,
    'heading_corrections': 0,
    'active_aircraft': 0,
    'data_source': 'json_files' if USE_JSON_FILES else 'dump1090'
}

_aircraft_state = {}  # Uçak state'leri (hex_id -> PositionValidator)
_connected_clients = set()  # WebSocket bağlı clientler