#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ADS-B Tracker - Otomatik Kurulum ve Başlatma
"""

import os
import sys
import subprocess
from pathlib import Path


def print_banner():
    """Hoş geldin banner'ı"""
    banner = """
    ╔═══════════════════════════════════════╗
    ║   🛩️  ADS-B TRACKER                   ║
    ║   Anti-Outlier Version 2.0           ║
    ╚═══════════════════════════════════════╝
    """
    print(banner)


def check_python_version():
    """Python versiyonunu kontrol et"""
    print("🔍 Python versiyonu kontrol ediliyor...")

    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 veya üstü gerekli!")
        print(f"   Mevcut versiyon: {version.major}.{version.minor}.{version.micro}")
        sys.exit(1)

    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")


def check_directories():
    """Gerekli klasörleri kontrol et"""
    print("\n📁 Klasörler kontrol ediliyor...")

    required_dirs = ['json_files', 'templates', 'static']
    project_root = Path(__file__).parent

    for dir_name in required_dirs:
        dir_path = project_root / dir_name
        if not dir_path.exists():
            print(f"⚠️  '{dir_name}' klasörü bulunamadı, oluşturuluyor...")
            dir_path.mkdir(exist_ok=True)
        else:
            print(f"✅ {dir_name}/ - OK")

    # JSON dosyalarını kontrol et
    json_files = list((project_root / 'json_files').glob('*.json'))
    if not json_files:
        print("\n⚠️  UYARI: json_files/ klasöründe JSON dosyası bulunamadı!")
        print("   Lütfen ADS-B JSON dosyalarınızı buraya yerleştirin.")
        response = input("\n   Devam etmek istiyor musunuz? (e/h): ")
        if response.lower() != 'e':
            sys.exit(0)
    else:
        print(f"✅ {len(json_files)} JSON dosyası bulundu")


def check_required_files():
    """Gerekli dosyaları kontrol et"""
    print("\n📄 Dosyalar kontrol ediliyor...")

    required_files = [
        'app.py',
        'config.py',
        'json_reader.py',
        'position_validator.py',
        'utils.py',
        'requirements.txt',
        'templates/index.html'
    ]

    project_root = Path(__file__).parent
    missing_files = []

    for file_name in required_files:
        file_path = project_root / file_name
        if file_path.exists():
            print(f"✅ {file_name}")
        else:
            print(f"❌ {file_name} - EKSIK!")
            missing_files.append(file_name)

    if missing_files:
        print("\n❌ Eksik dosyalar var! Lütfen artifact'lardan indirin:")
        for f in missing_files:
            print(f"   - {f}")
        sys.exit(1)


def install_dependencies():
    """Bağımlılıkları yükle"""
    print("\n📦 Bağımlılıklar kontrol ediliyor...")

    try:
        # Flask'ın yüklü olup olmadığını kontrol et
        import flask
        print("✅ Bağımlılıklar zaten yüklü")
        return
    except ImportError:
        pass

    print("📥 Bağımlılıklar yükleniyor...")
    response = input("   requirements.txt'den yüklensin mi? (e/h): ")

    if response.lower() != 'e':
        print("⏭️  Bağımlılık yüklemesi atlandı")
        return

    try:
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'
        ])
        print("✅ Bağımlılıklar başarıyla yüklendi")
    except subprocess.CalledProcessError as e:
        print(f"❌ Bağımlılık yükleme hatası: {e}")
        print("   Manuel olarak yüklemeyi deneyin:")
        print("   pip install -r requirements.txt")
        sys.exit(1)


def check_port_available(port=5000):
    """Port'un kullanılabilir olup olmadığını kontrol et"""
    import socket

    print(f"\n🔌 Port {port} kontrol ediliyor...")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('localhost', port))
    sock.close()

    if result == 0:
        print(f"⚠️  Port {port} zaten kullanımda!")
        print("   Başka bir uygulama kapatın veya config.py'de port değiştirin.")

        response = input("\n   Yine de devam edilsin mi? (e/h): ")
        if response.lower() != 'e':
            sys.exit(1)
    else:
        print(f"✅ Port {port} kullanılabilir")


def show_config():
    """Mevcut yapılandırmayı göster"""
    print("\n⚙️  Yapılandırma:")

    try:
        import config
        print(f"   📂 Veri Kaynağı: {'JSON Dosyaları' if config.USE_JSON_FILES else 'dump1090 (Canlı)'}")
        print(f"   🎯 Max Hız: {config.MAX_SPEED_KTS} kts")
        print(f"   📏 Max Sıçrama: {config.MAX_JUMP_KM} km")
        print(f"   🔄 JSON Döngü: {'Evet' if config.JSON_LOOP else 'Hayır'}")
        print(f"   ⚡ Oynatma Hızı: {config.JSON_PLAYBACK_SPEED}x")
        print(f"   🐛 Debug Modu: {'Aktif' if config.DEBUG_MODE else 'Kapalı'}")
    except Exception as e:
        print(f"   ⚠️  Config okunamadı: {e}")


def start_application():
    """Uygulamayı başlat"""
    print("\n" + "=" * 50)
    print("🚀 UYGULAMA BAŞLATILIYOR...")
    print("=" * 50)
    print("\n📍 Tarayıcınızda açın: http://localhost:5000")
    print("⏹️  Durdurmak için: Ctrl+C\n")

    try:
        # app.py'yi çalıştır
        subprocess.run([sys.executable, 'app.py'])
    except KeyboardInterrupt:
        print("\n\n👋 Uygulama kapatıldı. Görüşmek üzere!")
    except Exception as e:
        print(f"\n❌ Hata: {e}")
        sys.exit(1)


def main():
    """Ana fonksiyon"""
    try:
        print_banner()

        # Kontroller
        check_python_version()
        check_directories()
        check_required_files()
        install_dependencies()
        check_port_available()
        show_config()

        # Başlatma onayı
        print("\n" + "=" * 50)
        response = input("🎮 Uygulamayı başlatmak için ENTER'a basın (q = çıkış): ")

        if response.lower() == 'q':
            print("👋 Çıkış yapıldı")
            sys.exit(0)

        # Başlat
        start_application()

    except KeyboardInterrupt:
        print("\n\n👋 İşlem iptal edildi")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Beklenmeyen hata: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()