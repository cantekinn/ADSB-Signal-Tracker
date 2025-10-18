# position_validator.py
import math
from collections import deque
from utils import haversine_km, implied_speed_kts, calculate_bearing, debug_log
import config


class PositionValidator:
    """Gelişmiş pozisyon doğrulama sınıfı - KALICI İZ DESTEĞİ"""

    def __init__(self, hex_id):
        self.hex_id = hex_id
        # DENGELİ ÇÖZÜM: maxlen=200 (yeterli + performanslı)
        self.position_history = deque(maxlen=config.POSITION_HISTORY_SIZE)
        self.last_valid_pos = None
        self.last_valid_track = None
        self.last_valid_speed = None
        self.outlier_count = 0
        self.total_updates = 0
        self.first_seen = None  # İlk görülme zamanı
        self.last_seen = None  # Son görülme zamanı

    def add_position(self, lat, lon, ts, track=None, speed=None):
        """Pozisyon ekle ve doğrula - İZ HİÇ SİLİNMEZ!"""
        self.total_updates += 1
        self.last_seen = ts

        pos = {
            'lat': lat, 'lon': lon, 'ts': ts,
            'track': track, 'speed': speed
        }

        if not self.position_history:
            # İlk pozisyon
            self.first_seen = ts
            self.position_history.append(pos)
            self.last_valid_pos = pos
            if track is not None:
                self.last_valid_track = track
            if speed is not None:
                self.last_valid_speed = speed
            return pos, False, "first_position"

        # Outlier testi
        is_outlier, reason = self._is_outlier(pos)

        if is_outlier:
            self.outlier_count += 1
            debug_log(f"🚫 {self.hex_id}: Outlier detected - {reason}")

            # Düzeltilmiş pozisyon döndür (ama history'e ekleme!)
            corrected_pos = self._get_corrected_position(pos)
            return corrected_pos, True, reason
        else:
            # Geçerli pozisyon - history'e ekle
            self.position_history.append(pos)
            self.last_valid_pos = pos
            if track is not None:
                self.last_valid_track = track
            if speed is not None:
                self.last_valid_speed = speed
            return pos, False, "valid"

    def _is_outlier(self, pos):
        """Pozisyon outlier mı kontrol et"""
        prev = self.position_history[-1]

        # Zaman kontrolü
        time_diff = pos['ts'] - prev['ts']
        if time_diff <= 0:
            return True, "backwards_time"

        if time_diff < config.MIN_TIME_DIFF:
            return True, "too_frequent"

        # Mesafe kontrolü
        distance = haversine_km(prev['lat'], prev['lon'], pos['lat'], pos['lon'])

        if distance > config.MAX_JUMP_KM:
            return True, f"big_jump_{distance:.1f}km"

        # Hız kontrolü
        speed_kts = implied_speed_kts(
            prev['lat'], prev['lon'], prev['ts'],
            pos['lat'], pos['lon'], pos['ts']
        )

        if speed_kts > config.MAX_SPEED_KTS:
            return True, f"overspeed_{speed_kts:.0f}kts"

        # İleri seviye outlier detection (3+ pozisyon varsa)
        if len(self.position_history) >= 3:
            recent_positions = list(self.position_history)[-3:]
            avg_lat = sum(p['lat'] for p in recent_positions) / 3
            avg_lon = sum(p['lon'] for p in recent_positions) / 3

            outlier_dist = haversine_km(avg_lat, avg_lon, pos['lat'], pos['lon'])

            if self.last_valid_speed:
                expected_max_dist = (self.last_valid_speed * 0.514444 * time_diff) / 1000
                expected_max_dist *= config.OUTLIER_SPEED_MULTIPLIER

                if outlier_dist > max(config.OUTLIER_DISTANCE_KM, expected_max_dist):
                    return True, f"pattern_outlier_{outlier_dist:.1f}km"

        return False, "valid"

    def _get_corrected_position(self, outlier_pos):
        """Outlier pozisyon için düzeltme yap"""
        if not self.last_valid_pos:
            return outlier_pos

        # Velocity-based prediction
        if len(self.position_history) >= 2 and self.last_valid_speed:
            prev1 = self.position_history[-2]
            prev2 = self.position_history[-1]

            dt = prev2['ts'] - prev1['ts']
            if dt > 0:
                bearing = calculate_bearing(prev1['lat'], prev1['lon'], prev2['lat'], prev2['lon'])

                if bearing is not None:
                    time_since_last = outlier_pos['ts'] - prev2['ts']
                    distance_km = (self.last_valid_speed * 0.514444 * time_since_last) / 1000

                    lat_rad = math.radians(prev2['lat'])
                    bearing_rad = math.radians(bearing)

                    # Yeni pozisyon hesapla
                    new_lat = prev2['lat'] + (distance_km / 111.32) * math.cos(bearing_rad)
                    new_lon = prev2['lon'] + (distance_km / (111.32 * math.cos(lat_rad))) * math.sin(bearing_rad)

                    debug_log(f"🔧 {self.hex_id}: Pozisyon velocity ile tahmin edildi")

                    return {
                        'lat': new_lat,
                        'lon': new_lon,
                        'ts': outlier_pos['ts'],
                        'track': self.last_valid_track,
                        'speed': self.last_valid_speed
                    }

        # Fallback: son geçerli pozisyonu döndür
        return {
            **self.last_valid_pos,
            'ts': outlier_pos['ts']
        }

    def get_movement_heading(self):
        """Gerçek hareket yönünü hesapla"""
        if len(self.position_history) < 2:
            return self.last_valid_track

        # Son iki pozisyondan bearing hesapla
        p1 = self.position_history[-2]
        p2 = self.position_history[-1]

        distance = haversine_km(p1['lat'], p1['lon'], p2['lat'], p2['lon'])

        if distance >= config.HEADING_CONFIDENCE_THRESHOLD:
            return calculate_bearing(p1['lat'], p1['lon'], p2['lat'], p2['lon'])

        return self.last_valid_track

    def get_trail_points(self, max_points=None):
        """İz noktalarını getir - TÜM NOKTALARI SAKLADIĞIMIZ İÇİN"""
        if max_points is None:
            max_points = config.AIRCRAFT_TRAIL['max_points']

        # Son N noktayı döndür
        all_points = list(self.position_history)
        if len(all_points) <= max_points:
            return all_points
        else:
            # En son max_points kadarını al
            return all_points[-max_points:]

    def get_total_distance(self):
        """Toplam kat edilen mesafe (km)"""
        if len(self.position_history) < 2:
            return 0.0

        total = 0.0
        for i in range(1, len(self.position_history)):
            p1 = self.position_history[i - 1]
            p2 = self.position_history[i]
            total += haversine_km(p1['lat'], p1['lon'], p2['lat'], p2['lon'])

        return total

    def get_flight_duration(self):
        """Uçuş süresi (saniye)"""
        if not self.first_seen or not self.last_seen:
            return 0
        return self.last_seen - self.first_seen