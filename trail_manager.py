# trail_manager.py
"""
Uçak izlerini SQLite database'de saklama ve yönetme
"""
import sqlite3
import json
from datetime import datetime
from pathlib import Path
import config
from utils import debug_log


class TrailManager:
    """Uçak izlerini database'de yönetir"""

    def __init__(self, db_path=None):
        self.db_path = db_path or config.DB_PATH
        self._init_database()

    def _init_database(self):
        """Database ve tabloları oluştur"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Trail points tablosu
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS trail_points (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    hex_id TEXT NOT NULL,
                    lat REAL NOT NULL,
                    lon REAL NOT NULL,
                    altitude REAL,
                    speed REAL,
                    track REAL,
                    timestamp REAL NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    INDEX idx_hex_timestamp (hex_id, timestamp)
                )
            """)

            # Trail metadata tablosu (özet bilgiler)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS trail_metadata (
                    hex_id TEXT PRIMARY KEY,
                    flight_code TEXT,
                    aircraft_type TEXT,
                    registration TEXT,
                    point_count INTEGER DEFAULT 0,
                    first_seen DATETIME,
                    last_seen DATETIME,
                    max_altitude REAL,
                    avg_speed REAL
                )
            """)

            conn.commit()
            conn.close()
            debug_log(f"✅ Database hazır: {self.db_path}")

        except Exception as e:
            debug_log(f"❌ Database init hatası: {e}", "ERROR")

    def save_trail_point(self, hex_id, lat, lon, timestamp, altitude=None,
                         speed=None, track=None, flight_code=None,
                         aircraft_type=None, registration=None):
        """Tek bir trail noktası kaydet"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Trail point ekle
            cursor.execute("""
                INSERT INTO trail_points 
                (hex_id, lat, lon, altitude, speed, track, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (hex_id, lat, lon, altitude, speed, track, timestamp))

            # Metadata güncelle
            cursor.execute("""
                INSERT INTO trail_metadata 
                (hex_id, flight_code, aircraft_type, registration, 
                 point_count, first_seen, last_seen, max_altitude, avg_speed)
                VALUES (?, ?, ?, ?, 1, datetime('now'), datetime('now'), ?, ?)
                ON CONFLICT(hex_id) DO UPDATE SET
                    point_count = point_count + 1,
                    last_seen = datetime('now'),
                    max_altitude = MAX(max_altitude, excluded.max_altitude),
                    avg_speed = (avg_speed * point_count + excluded.avg_speed) / (point_count + 1)
            """, (hex_id, flight_code, aircraft_type, registration,
                  altitude or 0, speed or 0))

            conn.commit()
            conn.close()

        except Exception as e:
            debug_log(f"❌ Trail kayıt hatası ({hex_id}): {e}", "ERROR")

    def get_trail(self, hex_id, limit=50):
        """Bir uçağın izini database'den getir"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT lat, lon, altitude, speed, track, timestamp
                FROM trail_points
                WHERE hex_id = ?
                ORDER BY timestamp DESC
                LIMIT ?
            """, (hex_id, limit))

            points = cursor.fetchall()
            conn.close()

            # Tersine çevir (eski -> yeni sıralama)
            return [
                {
                    'lat': p[0],
                    'lon': p[1],
                    'altitude': p[2],
                    'speed': p[3],
                    'track': p[4],
                    'timestamp': p[5]
                }
                for p in reversed(points)
            ]

        except Exception as e:
            debug_log(f"❌ Trail getirme hatası ({hex_id}): {e}", "ERROR")
            return []

    def get_trail_metadata(self, hex_id):
        """Uçağın trail meta bilgilerini getir"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT flight_code, aircraft_type, registration,
                       point_count, first_seen, last_seen,
                       max_altitude, avg_speed
                FROM trail_metadata
                WHERE hex_id = ?
            """, (hex_id,))

            row = cursor.fetchone()
            conn.close()

            if row:
                return {
                    'flight_code': row[0],
                    'aircraft_type': row[1],
                    'registration': row[2],
                    'point_count': row[3],
                    'first_seen': row[4],
                    'last_seen': row[5],
                    'max_altitude': row[6],
                    'avg_speed': row[7]
                }
            return None

        except Exception as e:
            debug_log(f"❌ Metadata getirme hatası: {e}", "ERROR")
            return None

    def cleanup_old_trails(self, hours=24):
        """Eski izleri temizle (varsayılan: 24 saat)"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Eski noktaları sil
            cursor.execute("""
                DELETE FROM trail_points
                WHERE created_at < datetime('now', '-' || ? || ' hours')
            """, (hours,))

            deleted_points = cursor.rowcount

            # Orphan metadata'ları temizle
            cursor.execute("""
                DELETE FROM trail_metadata
                WHERE hex_id NOT IN (SELECT DISTINCT hex_id FROM trail_points)
            """)

            deleted_metadata = cursor.rowcount

            conn.commit()
            conn.close()

            debug_log(f"🗑️ Temizlik: {deleted_points} nokta, {deleted_metadata} uçak silindi")

        except Exception as e:
            debug_log(f"❌ Temizlik hatası: {e}", "ERROR")

    def get_all_active_trails(self, hours=1):
        """Son X saat içinde aktif olan tüm uçakların izlerini getir"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT DISTINCT hex_id
                FROM trail_points
                WHERE created_at > datetime('now', '-' || ? || ' hours')
            """, (hours,))

            hex_ids = [row[0] for row in cursor.fetchall()]
            conn.close()

            # Her uçak için izleri getir
            trails = {}
            for hex_id in hex_ids:
                trails[hex_id] = self.get_trail(hex_id)

            return trails

        except Exception as e:
            debug_log(f"❌ Aktif izler getirme hatası: {e}", "ERROR")
            return {}

    def get_statistics(self):
        """Database istatistikleri"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Toplam nokta sayısı
            cursor.execute("SELECT COUNT(*) FROM trail_points")
            total_points = cursor.fetchone()[0]

            # Toplam uçak sayısı
            cursor.execute("SELECT COUNT(*) FROM trail_metadata")
            total_aircraft = cursor.fetchone()[0]

            # En uzun iz
            cursor.execute("""
                SELECT hex_id, point_count, flight_code
                FROM trail_metadata
                ORDER BY point_count DESC
                LIMIT 1
            """)
            longest_trail = cursor.fetchone()

            # Database boyutu
            db_size = Path(self.db_path).stat().st_size / (1024 * 1024)  # MB

            conn.close()

            return {
                'total_points': total_points,
                'total_aircraft': total_aircraft,
                'longest_trail': {
                    'hex_id': longest_trail[0] if longest_trail else None,
                    'point_count': longest_trail[1] if longest_trail else 0,
                    'flight_code': longest_trail[2] if longest_trail else None
                },
                'db_size_mb': round(db_size, 2)
            }

        except Exception as e:
            debug_log(f"❌ İstatistik hatası: {e}", "ERROR")
            return {}


# Singleton instance
_trail_manager = None


def get_trail_manager():
    """Global trail manager instance'ı döndür"""
    global _trail_manager
    if _trail_manager is None:
        _trail_manager = TrailManager()
    return _trail_manager