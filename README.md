# 🛩️ ADS-B Tracker Pro

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.1+-green.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

**Modern ve gelişmiş bir ADS-B uçak takip sistemi**

JSON kayıtlarından veya canlı dump1090'dan veri alıp, akıllı outlier detection ile gerçek zamanlı harita üzerinde görselleştirir.

 [Özellikler](#-özellikler) • [Kurulum](#-hızlı-başlangıç) • [Kullanım](#-kullanım) • [Katkıda Bulunma](#-katkıda-bulunma)

</div>


## ✨ Özellikler

### 🎯 Temel Özellikler
- 📡 **Çift Veri Kaynağı**: JSON dosyaları veya canlı dump1090 desteği
- 🗺️ **İnteraktif Harita**: Leaflet.js ile açık temalı canlı harita
- 🛤️ **Kalıcı Uçak İzleri**: Tıklama ile aktif, sınırsız iz saklama sistemi
- ✈️ **Profesyonel Uçak İkonları**: SVG tabanlı, yön gösterimli 3D-benzeri ikonlar
- 🛫 **Havaalanı Overlay**: Türkiye'deki tüm büyük havaalanları
- 📊 **Gerçek Zamanlı İstatistikler**: WebSocket ile anlık güncellemeler
- 🎨 **Modern UI**: Temiz ve kullanıcı dostu arayüz
- 📏 **Mesafe & Süre Hesaplama**: Toplam uçuş mesafesi ve süresi

### 🔬 İleri Seviye Özellikler
- ⚡ **Outlier Detection**: Anormal pozisyonları otomatik tespit ve düzeltme
- 🧭 **Movement-Based Heading**: Gerçek hareket yönü hesaplama
- 📈 **Position Validation**: Sınırsız geçmiş analizi ile doğrulama
- 🔄 **Smooth Transitions**: Pozisyon ve heading yumuşatma
- 🎯 **Bölge Filtreleme**: 400km yarıçap içinde akıllı filtreleme
- 📊 **Detaylı Metrikler**: Düzeltme ve anomali istatistikleri
- 💾 **Kalıcı İz Sistemi**: Uçuş başından sonuna tüm rotayı saklama

---

## 🚀 Hızlı Başlangıç

### Gereksinimler

- Python 3.8+
- pip (Python paket yöneticisi)

### 1. Projeyi İndirin

```bash
https://github.com/cantekinn/ADSB-Signal-Tracker
cd adsb-tracker-pro
```

### 2. Virtual Environment Oluşturun

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Bağımlılıkları Yükleyin

```bash
pip install -r requirements.txt
```

### 4. JSON Dosyalarını Yerleştirin

`json_files/` klasörüne ADS-B JSON dosyalarınızı koyun:

```
json_files/
├── adsb_data_0.json    # 0. saniye
├── adsb_data_5.json    # 5. saniye
├── adsb_data_10.json   # 10. saniye
└── ...
```

**JSON Format Örneği:**
```json
{
  "now": 1234567890.5,
  "aircraft": [
    {
      "hex": "abc123",
      "flight": "THY123",
      "lat": 41.0,
      "lon": 28.0,
      "altitude": 35000,
      "speed": 450,
      "track": 90
    }
  ]
}
```

### 5. Uygulamayı Başlatın

```bash
python start.py
```

veya doğrudan:

```bash
python app.py
```

### 6. Tarayıcıda Açın

**http://localhost:5000**

---

## ⚙️ Yapılandırma

`config.py` dosyasından ayarları özelleştirebilirsiniz:

```python
# Veri kaynağı seçimi
USE_JSON_FILES = True  # False = dump1090 canlı veri

# Görüntüleme
MAX_DISPLAYED_AIRCRAFT = 300  # Maksimum uçak sayısı
FOCUS_REGION = {
    'enabled': True,
    'center_lat': 40.0,
    'center_lon': 29.0,
    'radius_km': 400  # Bölge yarıçapı
}

# Outlier Detection
MAX_SPEED_KTS = 750.0      # Maksimum hız
MAX_JUMP_KM = 15.0         # Maksimum sıçrama mesafesi
OUTLIER_DISTANCE_KM = 8.0  # Anomali eşiği

# Playback
JSON_PLAYBACK_SPEED = 1.0  # Oynatma hızı (1.0 = normal)
JSON_LOOP = True           # Başa sarma
```

---

## 📖 Kullanım

### Web Arayüzü

1. **Uçak Bilgileri**: Uçak ikonuna tıklayarak detayları görüntüleyin
2. **Uçak İzi**: Popup'ta "🛤️ Uçak İzini Göster" butonuna tıklayın
3. **Kontroller**:
   - 🔄 **Başa Sar**: JSON playback'i sıfırlar
   - 🧹 **İzleri Temizle**: Tüm aktif izleri gizler
   - 📈 **Detaylar**: API istatistiklerini görüntüler

### API Endpoints

| Endpoint | Metod | Açıklama |
|----------|-------|----------|
| `/` | GET | Ana web arayüzü |
| `/api/stats` | GET | Detaylı istatistikler (JSON) |
| `/api/control/reset` | POST | Playback'i başa sar |

### WebSocket Events

```javascript
// Bağlantı
socket.on('connect', () => {
    console.log('Bağlandı');
});

// Uçak verisi
socket.on('update', (data) => {
    console.log('Uçaklar:', data.aircraft);
    console.log('İstatistikler:', data.stats);
});
```

---

## 🏗️ Proje Yapısı

```
adsb-tracker-pro/
├── app.py                   # Ana Flask uygulaması
├── config.py                # Yapılandırma ayarları
├── json_reader.py           # JSON dosya okuyucu
├── position_validator.py    # Pozisyon doğrulama motoru
├── utils.py                 # Yardımcı fonksiyonlar
├── start.py                 # Otomatik kurulum script'i
├── requirements.txt         # Python bağımlılıkları
├── .gitignore              # Git ignore kuralları
├── README.md               # Dokümantasyon
│
├── json_files/             # JSON veri dosyaları
│   └── adsb_data_*.json
│
├── templates/              # HTML şablonları
│   └── index.html
│
└── static/                 # Statik dosyalar
    ├── img/
    │   └── plane.png
    └── js/
        └── (kullanılmıyor)
```

---

## 🔧 Teknik Detaylar

### Outlier Detection Algoritması

1. **Hız Kontrolü**: `speed > MAX_SPEED_KTS` (750 knots)
2. **Sıçrama Kontrolü**: `distance > MAX_JUMP_KM` (15 km)
3. **Pattern Analizi**: Son 3 pozisyonun ortalamasından sapma
4. **Zaman Kontrolü**: `time_diff < MIN_TIME_DIFF` (0.3 saniye)

### Pozisyon Düzeltme

```python
# Velocity-based prediction
if outlier_detected:
    # Son 2 pozisyondan bearing hesapla
    bearing = calculate_bearing(pos1, pos2)
    
    # Hız ve zamana göre yeni pozisyon tahmin et
    predicted_pos = extrapolate(last_pos, bearing, speed, time_delta)
    
    return predicted_pos
```

### Movement Heading

```python
# Gerçek hareket yönü
if distance >= HEADING_CONFIDENCE_THRESHOLD:
    movement_heading = calculate_bearing(pos1, pos2)
    
    # ADS-B heading ile karşılaştır
    if abs(movement_heading - ads_b_heading) > 45:
        use_movement_heading()  # Daha güvenilir
```

---

## 📊 İstatistikler

Sistem şu metrikleri takip eder:

- **Active Aircraft**: Takip edilen uçak sayısı
- **Total Updates**: Toplam veri güncellemesi
- **Position Corrections**: Düzeltilen pozisyon sayısı
- **Heading Corrections**: Düzeltilen heading sayısı
- **Outliers Detected**: Tespit edilen anomali sayısı

API'den detaylı istatistiklere erişim:

```bash
curl http://localhost:5000/api/stats
```

---

## 🐛 Sorun Giderme

### Port zaten kullanımda

```bash
# config.py veya app.py'de port değiştirin
socketio.run(app, host="0.0.0.0", port=5001)
```

### JSON dosyaları okunamıyor

```bash
# Dosya formatını kontrol edin
python test_json.py

# Import kontrolü
python check_imports.py
```

### WebSocket bağlantı hatası

- CORS ayarlarını kontrol edin
- Firewall/antivirus kontrolü yapın
- `localhost` yerine `127.0.0.1` deneyin

---

## 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz! 

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'feat: Add amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request açın

### Commit Mesajları

- `feat:` - Yeni özellik
- `fix:` - Bug düzeltme
- `docs:` - Dokümantasyon
- `style:` - Kod formatı
- `refactor:` - Kod iyileştirme
- `test:` - Test ekleme
- `chore:` - Bakım işleri

---


## 🙏 Teşekkürler

- [Leaflet.js](https://leafletjs.com/) - İnteraktif harita
- [Flask](https://flask.palletsprojects.com/) - Web framework
- [Socket.IO](https://socket.io/) - WebSocket kütüphanesi
- [dump1090](https://github.com/flightaware/dump1090) - ADS-B decoder
- [CARTO](https://carto.com/) - Harita tile'ları

---

## 📧 İletişim

**Can Tekin**

- GitHub: https://github.com/cantekinn
- Email: cantekin943@gmail.com

---

<div align="center">

</div>
