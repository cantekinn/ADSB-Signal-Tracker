# app.py - ADS-B Tracker Pro
"""
Modern ADS-B aircraft tracking system with outlier detection
Author: Can Tekin
Version: 2.0.0
"""

import sys
import time
import threading
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
import requests

import config
from utils import debug_log
from position_validator import PositionValidator
from json_reader import get_json_reader

# UTF-8 desteği
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# =========================
# Flask + Socket.IO
# =========================
app = Flask(__name__, static_folder="static", template_folder="templates")
app.config['SECRET_KEY'] = 'adsb_tracker_pro_2025_secure_key'
app.config['JSON_SORT_KEYS'] = False

socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode="threading",
    logger=False,
    engineio_logger=False,
    ping_timeout=60,
    ping_interval=25
)


# =========================
# Ana Veri İşleme Fonksiyonu
# =========================
def sanitize_aircraft_positions(now_val, aircraft_list):
    """
    Uçak pozisyonlarını temizle, filtrele ve doğrula

    Args:
        now_val: Şu anki timestamp
        aircraft_list: Ham uçak verisi listesi

    Returns:
        Temizlenmiş ve doğrulanmış uçak listesi
    """
    from utils import smooth_angle, angle_difference

    cleaned_aircraft = []
    config._stats['total_updates'] = len(aircraft_list)
    position_corrections = 0
    heading_corrections = 0

    # Bölge filtresi aktifse
    if config.FOCUS_REGION['enabled']:
        from utils import haversine_km

        aircraft_with_distance = []
        for ac in aircraft_list:
            lat = ac.get("lat")
            lon = ac.get("lon")
            if lat is None or lon is None:
                continue

            distance = haversine_km(
                config.FOCUS_REGION['center_lat'],
                config.FOCUS_REGION['center_lon'],
                lat, lon
            )

            if distance <= config.FOCUS_REGION['radius_km']:
                aircraft_with_distance.append((distance, ac))

        # Mesafeye göre sırala
        aircraft_with_distance.sort(key=lambda x: x[0])
        filtered_count = len(aircraft_with_distance)
        aircraft_list = [ac for _, ac in aircraft_with_distance[:config.MAX_DISPLAYED_AIRCRAFT]]

        debug_log(
            f"🎯 Filtreleme: {len(aircraft_list)} uçak "
            f"({filtered_count} bölge içi, {config._stats['total_updates']} toplam)"
        )
    else:
        # Sadece limit uygula
        aircraft_list = aircraft_list[:config.MAX_DISPLAYED_AIRCRAFT]
        debug_log(f"🎯 Limit uygulandı: {len(aircraft_list)} uçak gösteriliyor")

    # Her uçak için
    for ac in aircraft_list:
        hex_id = (ac.get("hex") or "").lower()
        lat = ac.get("lat")
        lon = ac.get("lon")

        if not hex_id or lat is None or lon is None:
            continue

        seen = ac.get("seen", 0.0) or 0.0
        seen_pos = ac.get("seen_pos")
        ts_pos = (now_val - float(seen_pos)) if (seen_pos is not None) else (now_val - seen)

        # Validator al veya oluştur
        if hex_id not in config._aircraft_state:
            config._aircraft_state[hex_id] = PositionValidator(hex_id)

        validator = config._aircraft_state[hex_id]

        # Pozisyon doğrula
        corrected_pos, was_corrected, reason = validator.add_position(
            lat, lon, ts_pos,
            track=ac.get('track'),
            speed=ac.get('speed')
        )

        if was_corrected:
            position_corrections += 1
            config._stats['position_corrections'] += 1

        # Heading belirleme
        final_track = ac.get('track')

        if config.USE_MOVEMENT_HEADING:
            movement_heading = validator.get_movement_heading()

            if movement_heading is not None:
                if final_track is not None:
                    heading_diff = abs(angle_difference(movement_heading, final_track))

                    if heading_diff > 45:
                        debug_log(f"🧭 {hex_id}: Heading uyuşmazlığı {heading_diff:.1f}°")
                        final_track = movement_heading
                        heading_corrections += 1
                        config._stats['heading_corrections'] += 1
                    else:
                        final_track = smooth_angle(movement_heading, final_track, 0.7)
                else:
                    final_track = movement_heading

        # Heading yumuşatma
        if validator.last_valid_track is not None and final_track is not None:
            final_track = smooth_angle(
                validator.last_valid_track,
                final_track,
                config.TRACK_SMOOTH_ALPHA
            )

        # Uçak izi için pozisyon geçmişi (Akıllı downsampling)
        trail = []
        if config.AIRCRAFT_TRAIL['enabled'] and len(validator.position_history) > 1:
            max_trail_points = config.AIRCRAFT_TRAIL['max_points']
            all_points = list(validator.position_history)

            if len(all_points) > max_trail_points:
                # Akıllı downsampling: Her N noktadan 1'ini al
                step = max(1, len(all_points) // max_trail_points)
                sampled_points = all_points[::step][-max_trail_points:]
            else:
                sampled_points = all_points

            trail = [
                {'lat': p['lat'], 'lon': p['lon']}
                for p in sampled_points
            ]

        # Database'e kaydet (aktifse)
        if config.USE_SQLITE:
            try:
                from trail_manager import get_trail_manager
                trail_manager = get_trail_manager()

                if len(trail) > 0:
                    trail_manager.save_trail_point(
                        hex_id=hex_id,
                        lat=corrected_pos['lat'],
                        lon=corrected_pos['lon'],
                        timestamp=ts_pos,
                        altitude=ac.get('altitude') or ac.get('alt_baro') or ac.get('alt_geom'),
                        speed=ac.get('speed') or ac.get('gs'),
                        track=final_track,
                        flight_code=ac.get('flight'),
                        aircraft_type=ac.get('t'),
                        registration=ac.get('r')
                    )
            except ImportError:
                debug_log("⚠️ trail_manager.py bulunamadı, database desteği pasif", "WARNING")

        # Temiz uçak verisi
        cleaned_aircraft.append({
            **ac,
            "lat": corrected_pos['lat'],
            "lon": corrected_pos['lon'],
            "track": final_track,
            "_corrected": was_corrected,
            "_correction_reason": reason,
            "_movement_heading": validator.get_movement_heading(),
            "_trail": trail
        })

    # İstatistikler
    config._stats['active_aircraft'] = len(config._aircraft_state)
    config._stats['outliers_detected'] = sum(
        v.outlier_count for v in config._aircraft_state.values()
    )

    if position_corrections > 0 or heading_corrections > 0:
        debug_log(
            f"📊 {len(cleaned_aircraft)} uçak işlendi, "
            f"{position_corrections} pozisyon, "
            f"{heading_corrections} heading düzeltmesi"
        )

    # Eski uçakları temizle (10 dakikadan eski)
    cutoff_time = now_val - 600  # 10 dakika
    old_aircraft = [
        hex_id for hex_id, validator in config._aircraft_state.items()
        if validator.position_history and validator.position_history[-1]['ts'] < cutoff_time
    ]

    for hex_id in old_aircraft:
        debug_log(f"🗑️ Eski uçak silindi: {hex_id}")
        del config._aircraft_state[hex_id]

    return cleaned_aircraft


# =========================
# Veri Besleme Fonksiyonu
# =========================
def live_feed():
    """Ana veri akışı döngüsü"""
    debug_log("🚀 Canlı veri akışı başlatıldı")
    debug_log(f"📂 Veri kaynağı: {config._stats['data_source']}")

    # Database temizleme (her 1 saatte bir)
    if config.USE_SQLITE:
        def cleanup_thread():
            while True:
                time.sleep(3600)  # 1 saat
                try:
                    from trail_manager import get_trail_manager
                    trail_manager = get_trail_manager()
                    trail_manager.cleanup_old_trails(hours=24)
                except ImportError:
                    pass

        cleanup = threading.Thread(target=cleanup_thread, daemon=True)
        cleanup.start()

    if config.USE_JSON_FILES:
        feed_from_json()
    else:
        feed_from_dump1090()


def feed_from_json():
    """JSON dosyalarından veri besle"""
    json_reader = get_json_reader()

    while True:
        try:
            raw_data = json_reader.read_next_data()

            if raw_data is None:
                if not config.JSON_LOOP:
                    debug_log("ℹ️ JSON dosyaları tamamlandı")
                    break
                time.sleep(1)
                continue

            now_val = raw_data.get("now", time.time())
            planes = raw_data.get("aircraft", [])

            # Temel veri temizleme ve normalizasyon
            aircraft = []
            for a in planes:
                if a.get("lat") is None or a.get("lon") is None:
                    continue

                try:
                    # Alan isimlerini normalize et
                    altitude = a.get("altitude") or a.get("alt_baro") or a.get("alt_geom")
                    speed = a.get("speed") or a.get("gs")

                    aircraft.append({
                        "hex": (a.get("hex") or "").lower(),
                        "flight": (a.get("flight") or "").strip(),
                        "altitude": altitude,
                        "speed": speed,
                        "track": a.get("track"),
                        "lat": float(a.get("lat")),
                        "lon": float(a.get("lon")),
                        "seen": float(a.get("seen", 0.0)),
                        "seen_pos": a.get("seen_pos"),
                        "squawk": a.get("squawk"),
                        "type": a.get("type"),
                        "r": a.get("r"),  # Registration
                        "t": a.get("t")  # Aircraft type
                    })
                except (ValueError, TypeError) as e:
                    debug_log(f"⚠️ Uçak verisi parse hatası: {e}", "WARNING")
                    continue

            # Pozisyon filtreleme
            aircraft_clean = sanitize_aircraft_positions(now_val, aircraft)

            # Client'lara gönder
            if config._connected_clients and aircraft_clean:
                progress = json_reader.get_progress()
                payload = {
                    "now": now_val,
                    "aircraft": aircraft_clean,
                    "stats": {
                        **config._stats,
                        "progress": progress
                    }
                }
                socketio.emit("update", payload)

            # Hız kontrolü
            time.sleep(5.0 / config.JSON_PLAYBACK_SPEED)

        except Exception as e:
            debug_log(f"❌ JSON feed hatası: {e}", "ERROR")
            import traceback
            traceback.print_exc()
            time.sleep(1)


def feed_from_dump1090():
    """dump1090'dan canlı veri besle"""
    consecutive_errors = 0
    max_errors = 5

    while True:
        try:
            r = requests.get(config.DUMP1090_URL, timeout=8)
            r.raise_for_status()
            raw = r.json()

            consecutive_errors = 0  # Reset error counter

            now_val = raw.get("now", time.time())
            planes = raw.get("aircraft", [])

            # Temel veri temizleme
            aircraft = []
            for a in planes:
                if a.get("lat") is None or a.get("lon") is None:
                    continue

                try:
                    altitude = a.get("altitude") or a.get("alt_baro") or a.get("alt_geom")
                    speed = a.get("speed") or a.get("gs")

                    aircraft.append({
                        "hex": (a.get("hex") or "").lower(),
                        "flight": (a.get("flight") or "").strip(),
                        "altitude": altitude,
                        "speed": speed,
                        "track": a.get("track"),
                        "lat": float(a.get("lat")),
                        "lon": float(a.get("lon")),
                        "seen": float(a.get("seen", 0.0)),
                        "seen_pos": a.get("seen_pos"),
                        "squawk": a.get("squawk"),
                        "type": a.get("type"),
                        "r": a.get("r"),
                        "t": a.get("t")
                    })
                except (ValueError, TypeError):
                    continue

            aircraft_clean = sanitize_aircraft_positions(now_val, aircraft)

            if config._connected_clients and aircraft_clean:
                payload = {
                    "now": now_val,
                    "aircraft": aircraft_clean,
                    "stats": config._stats
                }
                socketio.emit("update", payload)

        except requests.exceptions.RequestException as e:
            consecutive_errors += 1
            debug_log(f"⚠️ Dump1090 bağlantı hatası ({consecutive_errors}/{max_errors}): {e}", "ERROR")

            if consecutive_errors >= max_errors:
                debug_log("❌ Çok fazla hata, 30 saniye bekleniyor...", "ERROR")
                time.sleep(30)
                consecutive_errors = 0
        except Exception as e:
            debug_log(f"❌ Dump1090 feed hatası: {e}", "ERROR")
            import traceback
            traceback.print_exc()

        time.sleep(config.POLL_INTERVAL)


# =========================
# Socket.IO Events
# =========================
@socketio.on("connect")
def on_connect():
    """Client bağlandı"""
    client_id = request.sid
    config._connected_clients.add(client_id)
    debug_log(f"🔌 Client bağlandı: {client_id} (toplam: {len(config._connected_clients)})")

    # İlk bağlantıda mevcut uçakları gönder
    socketio.emit("initial_data", {
        "stats": config._stats,
        "connected": True
    }, room=client_id)


@socketio.on("disconnect")
def on_disconnect():
    """Client ayrıldı"""
    client_id = request.sid
    config._connected_clients.discard(client_id)
    debug_log(f"🔌 Client ayrıldı: {client_id} (toplam: {len(config._connected_clients)})")


@socketio.on("ping")
def on_ping():
    """Ping-pong heartbeat"""
    socketio.emit("pong", {"timestamp": time.time()})


# =========================
# Flask Routes
# =========================
@app.route("/")
def index():
    """Ana sayfa"""
    return render_template("index.html")


@app.route("/api/stats")
def api_stats():
    """Detaylı istatistikler (JSON)"""
    aircraft_debug = {}

    for hex_id, validator in config._aircraft_state.items():
        if validator.position_history:
            latest = validator.position_history[-1]
            aircraft_debug[hex_id] = {
                "position_count": len(validator.position_history),
                "outlier_count": validator.outlier_count,
                "outlier_rate": f"{(validator.outlier_count / validator.total_updates * 100):.1f}%"
                if validator.total_updates > 0 else "0%",
                "last_position": {
                    "lat": round(latest['lat'], 6),
                    "lon": round(latest['lon'], 6),
                    "age_seconds": round(time.time() - latest['ts'], 1)
                },
                "last_track": validator.last_valid_track,
                "movement_heading": validator.get_movement_heading(),
                "total_distance_km": round(validator.get_total_distance(), 2),
                "flight_duration_seconds": int(validator.get_flight_duration())
            }

    # Progress bilgisi
    progress_info = None
    if config.USE_JSON_FILES:
        json_reader = get_json_reader()
        progress_info = json_reader.get_progress()

    # Database istatistikleri (aktifse)
    db_stats = None
    if config.USE_SQLITE:
        try:
            from trail_manager import get_trail_manager
            trail_manager = get_trail_manager()
            db_stats = trail_manager.get_statistics()
        except ImportError:
            pass

    return jsonify({
        "stats": config._stats,
        "aircraft": aircraft_debug,
        "connected_clients": len(config._connected_clients),
        "progress": progress_info,
        "database": db_stats,
        "config": {
            "data_source": config._stats['data_source'],
            "max_speed_kts": config.MAX_SPEED_KTS,
            "max_jump_km": config.MAX_JUMP_KM,
            "use_movement_heading": config.USE_MOVEMENT_HEADING,
            "use_sqlite": config.USE_SQLITE,
            "max_displayed_aircraft": config.MAX_DISPLAYED_AIRCRAFT
        },
        "timestamp": datetime.now().isoformat()
    })


@app.route("/api/control/reset", methods=['POST'])
def api_reset():
    """JSON okuyucuyu sıfırla"""
    if not config.USE_JSON_FILES:
        return jsonify({
            "success": False,
            "message": "JSON modu aktif değil (canlı mod çalışıyor)"
        })

    try:
        json_reader = get_json_reader()
        json_reader.reset()

        # İstatistikleri sıfırla
        config._stats['position_corrections'] = 0
        config._stats['heading_corrections'] = 0
        config._stats['outliers_detected'] = 0

        return jsonify({
            "success": True,
            "message": "✅ JSON okuyucu başa sarıldı"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"❌ Reset hatası: {str(e)}"
        })


@app.route("/api/trail/<hex_id>")
def api_get_trail(hex_id):
    """Bir uçağın izini database'den getir"""
    if not config.USE_SQLITE:
        return jsonify({
            "success": False,
            "message": "Database desteği aktif değil"
        })

    try:
        from trail_manager import get_trail_manager
        trail_manager = get_trail_manager()

        trail = trail_manager.get_trail(hex_id.lower(), limit=100)
        metadata = trail_manager.get_trail_metadata(hex_id.lower())

        return jsonify({
            "success": True,
            "hex_id": hex_id,
            "trail": trail,
            "metadata": metadata
        })
    except ImportError:
        return jsonify({
            "success": False,
            "message": "trail_manager.py bulunamadı"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        })


@app.route("/api/airports")
def api_airports():
    """Havaalanları listesi (GeoJSON)"""
    try:
        from airports import get_airports_geojson
        return jsonify(get_airports_geojson())
    except ImportError:
        return jsonify({
            "error": "airports.py bulunamadı",
            "type": "FeatureCollection",
            "features": []
        })


@app.route("/api/nearest-airport/<hex_id>")
def api_nearest_airport(hex_id):
    """Uçağa en yakın havaalanı"""
    try:
        from airports import get_nearest_airport

        # Uçak pozisyonunu bul
        validator = config._aircraft_state.get(hex_id.lower())
        if not validator or not validator.last_valid_pos:
            return jsonify({
                "success": False,
                "error": "Uçak bulunamadı veya pozisyon bilgisi yok"
            })

        lat = validator.last_valid_pos['lat']
        lon = validator.last_valid_pos['lon']

        nearest = get_nearest_airport(lat, lon)
        return jsonify({
            "success": True,
            "nearest_airport": nearest
        })

    except ImportError:
        return jsonify({
            "success": False,
            "error": "airports.py bulunamadı"
        })


@app.route("/api/health")
def api_health():
    """Sistem sağlık kontrolü"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "active_aircraft": len(config._aircraft_state),
        "connected_clients": len(config._connected_clients),
        "data_source": config._stats['data_source']
    })


# =========================
# Hata Yönetimi
# =========================
@app.errorhandler(404)
def not_found(error):
    """404 hatası"""
    return jsonify({"error": "Endpoint bulunamadı"}), 404


@app.errorhandler(500)
def internal_error(error):
    """500 hatası"""
    debug_log(f"❌ Internal server error: {error}", "ERROR")
    return jsonify({"error": "İç sunucu hatası"}), 500


# =========================
# Ana Çalıştırma
# =========================
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🛩️  ADS-B Tracker Pro - Enhanced Edition v2.0")
    print("=" * 60)
    print(f"📊 Yapılandırma:")
    print(f"   • Max jump: {config.MAX_JUMP_KM}km")
    print(f"   • Max speed: {config.MAX_SPEED_KTS}kts")
    print(f"   • Movement heading: {config.USE_MOVEMENT_HEADING}")
    print(f"   • Veri kaynağı: {config._stats['data_source']}")
    print(f"   • Database: {'Aktif' if config.USE_SQLITE else 'Pasif'}")
    print(f"   • İz sistemi: KALICI (sınırsız history)")
    print(f"   • Max uçak: {config.MAX_DISPLAYED_AIRCRAFT}")
    print(f"   • Bölge filtre: {config.FOCUS_REGION['radius_km']}km yarıçap")
    print("=" * 60)
    print(f"🌐 Server: http://0.0.0.0:5000")
    print(f"📱 Local: http://127.0.0.1:5000")
    print("=" * 60 + "\n")

    # Feed thread'i başlat
    feed_thread = threading.Thread(target=live_feed, daemon=True)
    feed_thread.start()

    # Flask'ı başlat
    try:
        socketio.run(
            app,
            host="0.0.0.0",
            port=5000,
            debug=False,
            use_reloader=False
        )
    except KeyboardInterrupt:
        print("\n\n👋 Uygulama kapatılıyor...")
    except Exception as e:
        print(f"\n❌ Kritik hata: {e}")
        import traceback

        traceback.print_exc()