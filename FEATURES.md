# 🎨 Özellik Geliştirme Yol Haritası

## ✅ Mevcut Özellikler

- [x] Real-time aircraft tracking
- [x] Outlier detection & correction
- [x] Movement-based heading calculation
- [x] Click-to-show aircraft trails
- [x] Interactive aircraft info popups
- [x] WebSocket real-time updates
- [x] JSON playback mode
- [x] Region-based filtering (400km radius)
- [x] Light theme map

---

## 🚀 Öncelikli Özellikler (Sprint 1)

### 1. Gelişmiş Filtreler 🎯
```python
# config.py
ADVANCED_FILTERS = {
    'altitude_range' (0, 50000),      # Min-max altitude (feet)
    'speed_range' (0, 800),           # Min-max speed (knots)
    'aircraft_types' [],              # Boşsa hepsi (örn ['B77W', 'A333'])
    'only_commercial' False,          # Sadece ticari uçaklar
    'exclude_military' True,          # Askeri uçakları hariç tut
}
```

Frontend'de
```html
div class=filter-panel
    h3🎛️ Filtrelerh3
    labelYükseklik (ft)label
    input type=range id=minAlt min=0 max=50000
    
    labelHız (kts)label
    input type=range id=minSpeed min=0 max=800
    
    labelUçak Tipilabel
    select id=aircraftType
        option value=allTümüoption
        option value=B77WBoeing 777option
        option value=A333Airbus A330option
    select
div
```

### 2. Havaalanı Overlay 🛫
```python
# airports.py
MAJOR_AIRPORTS = {
    'LTFM' {'name' 'Istanbul Airport', 'lat' 41.2619, 'lon' 28.7419},
    'LTAC' {'name' 'Esenboğa Airport', 'lat' 40.1281, 'lon' 32.9951},
    'LTAI' {'name' 'Antalya Airport', 'lat' 36.8987, 'lon' 30.8005},
}
```

Frontend'de marker'lar
```javascript
Object.values(airports).forEach(airport = {
    L.marker([airport.lat, airport.lon], {
        icon airportIcon
    }).addTo(map)
    .bindPopup(`b🛫 ${airport.name}b`);
});
```

### 3. Uçak Arama 🔍
```html
input type=text id=searchAircraft 
       placeholder=ICAO hex, flight code, veya registration...
```

```javascript
function searchAircraft(query) {
    const aircraft = Object.values(aircraftMarkers).find(marker = {
        const ac = marker.aircraft;
        return ac.hex.includes(query)  
               ac.flight.includes(query) 
               ac.r.includes(query);
    });
    
    if (aircraft) {
        map.flyTo(aircraft.getLatLng(), 10);
        aircraft.openPopup();
    }
}
```

### 4. Mesafe & ETA Hesaplama 📏
```javascript
 Havaalanına olan mesafe ve varış tahmini
function calculateETA(aircraft, airport) {
    const distance = haversine(aircraft.lat, aircraft.lon, 
                              airport.lat, airport.lon);
    const eta = distance  (aircraft.speed  1.852);  saat
    
    return {
        distance_km distance,
        distance_nm distance  0.539957,
        eta_hours eta,
        eta_time new Date(Date.now() + eta  3600000)
    };
}
```

---

## 🎨 Orta Öncelikli Özellikler (Sprint 2)

### 5. Heatmap Görünümü 🔥
```javascript
 Uçak yoğunluğu heatmap'i
const heatData = aircraft.map(ac = [ac.lat, ac.lon, 1]);
const heatLayer = L.heatLayer(heatData, {
    radius 25,
    blur 15,
    maxZoom 10
}).addTo(map);
```

### 6. 3D Yükseklik Profili 📊
```javascript
 Chart.js ile altitude profile
const altitudeChart = new Chart(ctx, {
    type 'line',
    data {
        labels trail.map(p = p.timestamp),
        datasets [{
            label 'Altitude (ft)',
            data trail.map(p = p.altitude),
            borderColor '#3b82f6',
            fill true
        }]
    }
});
```

### 7. Bildirim Sistemi 🔔
```javascript
 Belirli olaylar için bildirim
const NOTIFICATION_RULES = {
    low_altitude 1000,       1000 ft altına düşünce
    high_speed 600,          600 kts üstüne çıkınca
    squawk_7700 true,        Emergency squawk
};

function checkNotifications(aircraft) {
    if (aircraft.altitude  1000) {
        notify('⚠️ Düşük irtifa ' + aircraft.flight);
    }
    if (aircraft.squawk === '7700') {
        notify('🚨 EMERGENCY ' + aircraft.flight);
    }
}
```

### 8. Uçuş Geçmişi 📜
```python
@app.route(apiflighthistoryhex_id)
def flight_history(hex_id)
    Son 7 günün uçuş geçmişi
    trail_manager = get_trail_manager()
    
    # Son 7 gün
    history = trail_manager.get_flight_history(
        hex_id, 
        days=7
    )
    
    return jsonify({
        'flights' history,
        'total_flights' len(history),
        'total_distance_km' sum(f['distance'] for f in history)
    })
```

### 9. Dark Mode Toggle 🌓
```javascript
function toggleTheme() {
    const isDark = document.body.classList.toggle('dark-mode');
    
     Harita tile'ını değiştir
    map.removeLayer(lightTileLayer);
    
    if (isDark) {
        map.addLayer(darkTileLayer);
    } else {
        map.addLayer(lightTileLayer);
    }
    
    localStorage.setItem('theme', isDark  'dark'  'light');
}
```

### 10. Export  Share 📤
```javascript
function exportScreenshot() {
    html2canvas(document.querySelector('#map')).then(canvas = {
        canvas.toBlob(blob = {
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `adsb-tracker-${Date.now()}.png`;
            a.click();
        });
    });
}

function shareLink() {
    const url = new URL(window.location.href);
    url.searchParams.set('lat', map.getCenter().lat);
    url.searchParams.set('lon', map.getCenter().lon);
    url.searchParams.set('zoom', map.getZoom());
    
    navigator.clipboard.writeText(url.toString());
    notify('📋 Link kopyalandı!');
}
```

---

## 🌟 İleri Seviye Özellikler (Sprint 3)

### 11. Makine Öğrenimi Entegrasyonu 🤖
```python
# ml_predictor.py
import tensorflow as tf

class FlightPredictor
    Uçuş rotası ve varış zamanı tahmini
    
    def predict_route(self, trail)
        # Son 10 pozisyondan sonraki 5 pozisyonu tahmin et
        model = tf.keras.models.load_model('modelsroute_predictor.h5')
        
        features = self._extract_features(trail)
        predictions = model.predict(features)
        
        return predictions
```

### 12. Gerçek Zamanlı Hava Durumu ☁️
```python
# weather.py
import requests

def get_weather_at_position(lat, lon)
    OpenWeather API kullanarak hava durumu
    api_key = config.OPENWEATHER_API_KEY
    url = fhttpsapi.openweathermap.orgdata2.5weather
    
    response = requests.get(url, params={
        'lat' lat,
        'lon' lon,
        'appid' api_key
    })
    
    return response.json()
```

### 13. Çarpışma Uyarısı ⚠️
```python
def detect_collision_risk(aircraft_list)
    Potansiyel çarpışmaları tespit et
    warnings = []
    
    for i, ac1 in enumerate(aircraft_list)
        for ac2 in aircraft_list[i+1]
            distance = haversine_km(ac1['lat'], ac1['lon'], 
                                   ac2['lat'], ac2['lon'])
            alt_diff = abs(ac1.get('altitude', 0) - ac2.get('altitude', 0))
            
            # 5km mesafe ve 1000ft altitude farkı içindeyse
            if distance  5 and alt_diff  1000
                warnings.append({
                    'aircraft1' ac1['hex'],
                    'aircraft2' ac2['hex'],
                    'distance_km' distance,
                    'altitude_diff_ft' alt_diff,
                    'risk_level' 'HIGH' if distance  2 else 'MEDIUM'
                })
    
    return warnings
```

### 14. Ses Bildirimleri 🔊
```javascript
 Text-to-Speech
function announceAircraft(aircraft) {
    const speech = new SpeechSynthesisUtterance(
        `${aircraft.flight} approaching at ${aircraft.altitude} feet`
    );
    speechSynthesis.speak(speech);
}
```

### 15. Multi-User Chat 💬
```javascript
 Socket.IO ile chat sistemi
socket.on('chat_message', (msg) = {
    appendChatMessage(msg.user, msg.message);
});

function sendChatMessage(message) {
    socket.emit('chat_message', {
        user currentUser,
        message message,
        timestamp Date.now()
    });
}
```

---

## 📱 Mobil Özellikler

### 16. Progressive Web App (PWA) 📲
```json
 manifest.json
{
  name ADS-B Tracker Pro,
  short_name ADS-B,
  start_url ,
  display standalone,
  background_color #ffffff,
  theme_color #3b82f6,
  icons [
    {
      src staticimgicon-192.png,
      sizes 192x192,
      type imagepng
    }
  ]
}
```

### 17. GPS Konumunu Kullan 📍
```javascript
if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(pos = {
        const userLat = pos.coords.latitude;
        const userLon = pos.coords.longitude;
        
         Haritayı kullanıcı konumuna getir
        map.setView([userLat, userLon], 10);
        
         En yakın uçağı bul
        findNearestAircraft(userLat, userLon);
    });
}
```

---

## 🎯 Uygulama Öncelikleri

### Hemen (1-2 hafta)
- [x] ✅ Açık tema (TAMAMLANDI)
- [x] ✅ Tıklama ile iz gösterme (TAMAMLANDI)
- [ ] 🔄 Gelişmiş filtreler
- [ ] 🔄 Havaalanı overlay
- [ ] 🔄 Uçak arama

### Kısa Vadeli (1 ay)
- [ ] Heatmap görünümü
- [ ] 3D yükseklik profili
- [ ] Bildirim sistemi
- [ ] Dark mode toggle
- [ ] ExportShare

### Orta Vadeli (2-3 ay)
- [ ] ML rota tahmini
- [ ] Hava durumu entegrasyonu
- [ ] Çarpışma uyarısı
- [ ] PWA desteği

### Uzun Vadeli (6+ ay)
- [ ] Multi-user chat
- [ ] Mobil uygulama (React Native)
- [ ] API marketplace
- [ ] Enterprise features