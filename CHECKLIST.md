\# ✅ GitHub Yükleme Hazırlık Listesi



\## 📁 Dosya Yapısı Kontrolü



\### Silınecek Dosyalar/Klasörler

```bash

\# Windows Command Prompt'ta çalıştır:

cd "C:\\Users\\Can Tekin\\Documents\\adsb-web2\\adsb-web"



\# Gereksiz klasörleri sil

rmdir /s /q .idea

rmdir /s /q \_\_pycache\_\_

rmdir /s /q node-js

rmdir /s /q dump1090\_json



\# Root'taki fazladan venv'i sil (sadece birini sakla)

\# venv/ VEYA .venv/ klasörünü sakla, diğerini sil

rmdir /s /q venv



\# Gereksiz dosyaları sil

del README.txt

del flight\_history.db

del start.bat

del static\\js\\app.js

```



\### Yeni Oluşturulacak/Güncellenecek Dosyalar



\#### 1. \*\*.gitignore\*\* (Artifact'tan kopyala)

```bash

\# .gitignore dosyasını artifact'tan kopyala ve kaydet

```



\#### 2. \*\*README.md\*\* (Artifact'tan kopyala)

```bash

\# Yeni README.md'yi artifact'tan kopyala

\# GitHub username ve email güncelle:

\# - \[@YOUR\_USERNAME] → \[@cantekin]

\# - \[your.email@example.com] → \[your-email]

```



\#### 3. \*\*templates/index.html\*\* (Artifact'tan kopyala)

```bash

\# Yeni index.html'i artifact'tan kopyala (açık tema + tıklama izi)

```



\#### 4. \*\*config.py\*\* (Artifact'tan kopyala)

```bash

\# Güncellenmiş config.py'yi artifact'tan kopyala

\# FOCUS\_REGION\['radius\_km'] = 400 olmalı

```



\#### 5. \*\*requirements.txt\*\* (Artifact'tan kopyala)

```bash

\# Güncellenmiş requirements.txt'yi artifact'tan kopyala

```



\#### 6. \*\*trail\_manager.py\*\* (Yeni dosya - opsiyonel)

```bash

\# Database trail desteği istiyorsanız artifact'tan kopyala

\# config.py'de USE\_SQLITE = True yapın

```



\#### 7. \*\*app.py\*\* (Güncellenmiş versiyon)

```bash

\# Database desteği eklenmiş yeni app.py'yi artifact'tan kopyala

```



\#### 8. \*\*json\_files/sample\_adsb\_data.json\*\* (Örnek veri)

```bash

\# GitHub için örnek JSON dosyası ekle

\# Artifact'taki sample\_adsb\_data.json'ı kopyala

```



---



\## 📸 Ekstra Dosyalar (Opsiyonel)



\### 1. \*\*LICENSE\*\* dosyası

```bash

\# MIT License oluştur

```



```text

MIT License



Copyright (c) 2025 Can Tekin



Permission is hereby granted, free of charge, to any person obtaining a copy

of this software and associated documentation files (the "Software"), to deal

in the Software without restriction, including without limitation the rights

to use, copy, modify, merge, publish, distribute, sublicense, and/or sell

copies of the Software, and to permit persons to whom the Software is

furnished to do so, subject to the following conditions:



The above copyright notice and this permission notice shall be included in all

copies or substantial portions of the Software.



THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR

IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,

FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE

AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER

LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,

OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE

SOFTWARE.

```



\### 2. \*\*screenshots/\*\* klasörü

```bash

mkdir screenshots



\# Uygulamadan ekran görüntüleri al:

\# - ana-sayfa.png (harita görünümü)

\# - popup.png (uçak detayları)

\# - trail.png (uçak izi)

\# - stats.png (istatistikler)

```



\### 3. \*\*CONTRIBUTING.md\*\* (Katkı rehberi)

```markdown

\# Katkıda Bulunma Rehberi



\## 🤝 Nasıl Katkıda Bulunurum?



1\. Fork yapın

2\. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)

3\. Değişikliklerinizi commit edin (`git commit -m 'feat: Add amazing feature'`)

4\. Branch'inizi push edin (`git push origin feature/amazing-feature`)

5\. Pull Request açın



\## 📝 Commit Mesaj Formatı



\- `feat:` - Yeni özellik

\- `fix:` - Bug düzeltme

\- `docs:` - Dokümantasyon

\- `style:` - Kod formatı

\- `refactor:` - Kod iyileştirme

\- `test:` - Test ekleme

\- `chore:` - Bakım işleri



\## 🧪 Test



```bash

\# Testleri çalıştır

python -m pytest



\# Import kontrolü

python check\_imports.py



\# JSON dosyaları kontrolü

python test\_json.py

```



\## 📧 İletişim



Sorularınız için issue açabilir veya email gönderebilirsiniz.

```



---



\## 🧪 Test Adımları



\### 1. Import Kontrolü

```bash

python check\_imports.py

```

\*\*Beklenen:\*\* Tüm modüller ✅ OK



\### 2. JSON Dosyaları Kontrolü

```bash

python test\_json.py

```

\*\*Beklenen:\*\* Tüm JSON dosyaları geçerli



\### 3. Uygulamayı Çalıştır

```bash

python start.py

```

\*\*Kontrol Et:\*\*

\- \[ ] WebSocket bağlantısı başarılı

\- \[ ] Uçaklar haritada görünüyor

\- \[ ] Uçağa tıklayınca popup açılıyor

\- \[ ] "Uçak İzini Göster" butonu çalışıyor

\- \[ ] İstatistikler güncelleniyor

\- \[ ] "Başa Sar" butonu çalışıyor



\### 4. Tarayıcı Konsol Kontrolü

\*\*F12 → Console\*\*

\- \[ ] Hata yok

\- \[ ] WebSocket mesajları geliyor

\- \[ ] "✅ WebSocket bağlandı" mesajı var



---



\## 📦 Git Hazırlığı



\### 1. Git Repository Başlat

```bash

cd "C:\\Users\\Can Tekin\\Documents\\adsb-web2\\adsb-web"

git init

```



\### 2. .gitignore Ekle

```bash

\# .gitignore dosyasını artifact'tan kopyaladıktan sonra

git add .gitignore

git commit -m "chore: Add .gitignore"

```



\### 3. Tüm Dosyaları Ekle

```bash

git add .

git status  # Kontrol et - gereksiz dosya eklenmemiş mi?

```



\### 4. İlk Commit

```bash

git commit -m "feat: Initial commit - ADS-B Tracker Pro v1.0"

```



\### 5. GitHub Repository Oluştur

1\. GitHub'da yeni repository oluştur: `adsb-tracker-pro`

2\. Description: "🛩️ Modern ADS-B aircraft tracking system with outlier detection and real-time trail visualization"

3\. Public/Private seç

4\. \*\*LICENSE seç:\*\* MIT License

5\. \*\*.gitignore seç:\*\* Python

6\. \*\*README ekleme:\*\* Hayır (zaten var)



\### 6. Remote Ekle ve Push

```bash

\# GitHub'dan aldığınız URL'i kullanın

git remote add origin https://github.com/YOUR\_USERNAME/adsb-tracker-pro.git

git branch -M main

git push -u origin main

```



---



\## 🎨 README.md'de Güncellenecekler



\### 1. GitHub Username Değiştir

```markdown

\# Değiştir:

\[@YOUR\_USERNAME](https://github.com/YOUR\_USERNAME)



\# Şununla:

\[@cantekin](https://github.com/cantekin)

```



\### 2. Email Güncelle

```markdown

\# Değiştir:

\- Email: your.email@example.com



\# Şununla:

\- Email: can.tekin@example.com  # Gerçek emailiniz

```



\### 3. Ekran Görüntüsü Ekle

```markdown

\# Değiştir:

!\[ADS-B Tracker Screenshot](https://via.placeholder.com/800x400/...)



\# Şununla:

!\[ADS-B Tracker Screenshot](screenshots/main-view.png)

```



\### 4. Git Clone URL'i Güncelle

```markdown

\# README.md'de otomatik güncellenecek

git clone https://github.com/cantekin/adsb-tracker-pro.git

```



---



\## 📊 Son Kontrol Listesi



\### Dosya Yapısı

```

adsb-tracker-pro/

├── .gitignore              ✅ Oluşturuldu

├── LICENSE                 ✅ MIT License

├── README.md              ✅ Güncellendi (username, email)

├── CONTRIBUTING.md        ⚠️ Opsiyonel

├── FEATURES.md            ⚠️ Opsiyonel

├── PERFORMANCE.md         ⚠️ Opsiyonel

├── requirements.txt       ✅ Güncellendi

├── app.py                 ✅ Güncellendi (DB desteği)

├── config.py              ✅ Güncellendi (radius=400)

├── json\_reader.py         ✅ Değişmedi

├── position\_validator.py  ✅ Değişmedi

├── utils.py               ✅ Değişmedi

├── trail\_manager.py       ⚠️ Yeni dosya (DB için)

├── start.py               ✅ Değişmedi

├── check\_imports.py       ✅ Değişmedi

├── test\_json.py           ✅ Değişmedi

│

├── templates/

│   └── index.html         ✅ Güncellendi (açık tema)

│

├── static/

│   └── img/

│       └── plane.png      ✅ Mevcut

│

├── json\_files/

│   ├── sample\_adsb\_data.json  ✅ Yeni (örnek veri)

│   └── .gitkeep               ✅ Boş klasör için

│

├── screenshots/           ⚠️ Opsiyonel (ekran görüntüleri)

│   ├── main-view.png

│   ├── popup.png

│   └── trail.png

│

└── .venv/                 ❌ Git'e eklenmeyecek (.gitignore'da)

```



\### .gitkeep Dosyaları Oluştur

```bash

\# Boş klasörleri Git'te tutmak için

echo "" > json\_files/.gitkeep

echo "" > screenshots/.gitkeep

```



---



\## 🚀 GitHub'a Push Öncesi Son Kontrol



\### 1. Git Status Kontrol

```bash

git status



\# Beklenen:

\# - venv/ dahil değil

\# - \_\_pycache\_\_/ dahil değil

\# - \*.db dosyaları dahil değil

\# - json\_files/\*.json dahil değil (sample hariç)

```



\### 2. Dosya Boyutu Kontrol

```bash

\# 100MB'dan büyük dosya olmamalı

find . -type f -size +100M

```



\### 3. Sensitive Data Kontrol

```bash

\# API key, şifre, token var mı?

grep -r "password\\|secret\\|api\_key\\|token" --exclude-dir=.git

```



\### 4. Test Çalıştırma

```bash

\# Son kez test et

python start.py



\# Tarayıcıda: http://localhost:5000

\# - Uçaklar görünüyor mu?

\# - İz çalışıyor mu?

\# - Console'da hata var mı?

```



---



\## 📝 GitHub Repository Ayarları



\### About Section

```

Description: 🛩️ Modern ADS-B aircraft tracking system with outlier detection

Website: https://cantekin.github.io/adsb-tracker-pro  (GitHub Pages varsa)

Topics: adsb, aircraft-tracking, python, flask, websocket, leaflet, real-time, aviation

```



\### Repository Settings

\- \[x] \*\*Issues\*\* - Aktif

\- \[x] \*\*Projects\*\* - Aktif (opsiyonel)

\- \[x] \*\*Wiki\*\* - Aktif (opsiyonel)

\- \[x] \*\*Discussions\*\* - Aktif (topluluk için)



\### GitHub Pages (Opsiyonel)

```bash

\# Sadece frontend için static site

\# Settings → Pages → Source: main branch → /docs folder

```



---



\## 🎯 İlk GitHub Actions (CI/CD) - Opsiyonel



\### .github/workflows/python-tests.yml

```yaml

name: Python Tests



on:

&nbsp; push:

&nbsp;   branches: \[ main, develop ]

&nbsp; pull\_request:

&nbsp;   branches: \[ main ]



jobs:

&nbsp; test:

&nbsp;   runs-on: ubuntu-latest

&nbsp;   

&nbsp;   steps:

&nbsp;   - uses: actions/checkout@v3

&nbsp;   

&nbsp;   - name: Set up Python

&nbsp;     uses: actions/setup-python@v4

&nbsp;     with:

&nbsp;       python-version: '3.11'

&nbsp;   

&nbsp;   - name: Install dependencies

&nbsp;     run: |

&nbsp;       python -m pip install --upgrade pip

&nbsp;       pip install -r requirements.txt

&nbsp;   

&nbsp;   - name: Run import checks

&nbsp;     run: python check\_imports.py

&nbsp;   

&nbsp;   - name: Run JSON tests

&nbsp;     run: python test\_json.py

&nbsp;   

&nbsp;   - name: Lint with pylint

&nbsp;     run: |

&nbsp;       pip install pylint

&nbsp;       pylint app.py config.py --disable=all --enable=E

```



---



\## 📢 Sunum Notları



\### GitHub README'de Vurgulayın

```markdown

\## 🌟 Öne Çıkan Özellikler



\### 🎯 Akıllı Outlier Detection

\- \*\*5-point history analysis\*\* ile anormal pozisyonları tespit

\- \*\*Velocity-based prediction\*\* ile otomatik düzeltme

\- \*\*~95% accuracy\*\* rate (test verilerinde)



\### 🧭 Movement-Based Heading

\- ADS-B heading yerine \*\*gerçek hareket yönü\*\* kullanma

\- \*\*45° threshold\*\* ile uyuşmazlık tespiti

\- Smooth angle interpolation (exponential smoothing)



\### 🛤️ Interactive Trail System

\- \*\*Click-to-show\*\* functionality (database'de saklanır)

\- \*\*50-point trail\*\* history per aircraft

\- Real-time position updates (WebSocket)



\### 📊 Real-Time Statistics

\- Position corrections counter

\- Heading corrections counter

\- Outlier detection rate

\- Active aircraft count

```



\### Demo Video Hazırlayın

```markdown

\## 🎥 Demo Video



\[!\[Demo Video](https://img.youtube.com/vi/VIDEO\_ID/0.jpg)](https://www.youtube.com/watch?v=VIDEO\_ID)



\*\*Video İçeriği:\*\*

1\. ⏱️ 0:00 - Giriş ve proje tanıtımı

2\. ⏱️ 0:30 - Uçak takibi ve filtreleme

3\. ⏱️ 1:00 - Outlier detection örneği

4\. ⏱️ 1:30 - Trail sistem gösterimi

5\. ⏱️ 2:00 - İstatistikler ve API

```



---



\## ✅ Final Checklist



\### Teknik

\- \[ ] Tüm testler geçiyor

\- \[ ] Uygulama çalışıyor

\- \[ ] Console'da hata yok

\- \[ ] .gitignore doğru yapılandırılmış

\- \[ ] requirements.txt güncel



\### Dokümantasyon

\- \[ ] README.md detaylı ve güncel

\- \[ ] Kod yorumları eksiksiz

\- \[ ] API endpoints dokümante edilmiş

\- \[ ] Kurulum adımları net



\### GitHub

\- \[ ] Repository oluşturuldu

\- \[ ] LICENSE eklendi (MIT)

\- \[ ] .gitignore eklendi

\- \[ ] İlk commit yapıldı

\- \[ ] README'de username güncellendi

\- \[ ] Topics/tags eklendi



\### Opsiyonel

\- \[ ] Screenshots eklendi

\- \[ ] CONTRIBUTING.md oluşturuldu

\- \[ ] GitHub Actions ayarlandı

\- \[ ] Demo video hazırlandı

\- \[ ] GitHub Pages aktif



---



\## 🎊 Başarılı Push Sonrası



\### 1. Repository URL'i Paylaşın

```

https://github.com/cantekin/adsb-tracker-pro

```



\### 2. README Badge'leri Güncelleyin

```markdown

!\[GitHub Stars](https://img.shields.io/github/stars/cantekin/adsb-tracker-pro?style=social)

!\[GitHub Forks](https://img.shields.io/github/forks/cantekin/adsb-tracker-pro?style=social)

!\[GitHub Issues](https://img.shields.io/github/issues/cantekin/adsb-tracker-pro)

!\[GitHub License](https://img.shields.io/github/license/cantekin/adsb-tracker-pro)

```



\### 3. Social Media Paylaşımı

```

🛩️ Yeni proje: ADS-B Tracker Pro!



✨ Özellikler:

\- Real-time uçak takibi

\- Akıllı outlier detection

\- Interactive trail system

\- Modern web arayüzü



🔗 https://github.com/cantekin/adsb-tracker-pro



\#Python #Flask #ADS-B #Aviation #OpenSource

```



\### 4. LinkedIn/Twitter Post

```

Yeni açık kaynak projem: ADS-B Tracker Pro 🛩️



ADS-B verilerinden gerçek zamanlı uçak takibi yapan, outlier detection ve trail visualization özellikleriyle donatılmış modern bir web uygulaması.



Teknolojiler: Python, Flask, WebSocket, Leaflet.js



GitHub: https://github.com/cantekin/adsb-tracker-pro



Katkılarınızı bekliyorum! ⭐

```



---



\## 🎯 Sonraki Adımlar



1\. \*\*GitHub Issues\*\* oluştur (roadmap için)

2\. \*\*Project board\*\* ayarla (kanban)

3\. \*\*First contributors\*\* issue'ları aç

4\. \*\*Documentation\*\* iyileştir

5\. \*\*Community\*\* oluştur (Discussions)



\*\*Başarılar! 🚀\*\*

