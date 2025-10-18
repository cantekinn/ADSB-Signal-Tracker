#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
JSON Dosyalarını Test Et
"""

import json
from pathlib import Path


def test_json_files():
    """JSON dosyalarını kontrol et"""
    json_dir = Path("json_files")

    if not json_dir.exists():
        print("❌ json_files/ klasörü bulunamadı!")
        return False

    json_files = sorted(json_dir.glob("*.json"))

    if not json_files:
        print("❌ JSON dosyası bulunamadı!")
        return False

    print(f"✅ {len(json_files)} JSON dosyası bulundu\n")

    total_aircraft = 0
    valid_files = 0

    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Zorunlu alanları kontrol et
            if 'now' not in data:
                print(f"⚠️  {json_file.name}: 'now' alanı eksik")
                continue

            if 'aircraft' not in data:
                print(f"⚠️  {json_file.name}: 'aircraft' alanı eksik")
                continue

            aircraft = data['aircraft']

            # Pozisyon bilgisi olan uçakları say
            with_position = sum(1 for ac in aircraft if ac.get('lat') and ac.get('lon'))

            print(f"✅ {json_file.name}")
            print(f"   📊 Toplam uçak: {len(aircraft)}")
            print(f"   📍 Pozisyonlu: {with_position}")
            print(f"   ⏰ Timestamp: {data['now']}")

            # İlk uçağın detaylarını göster
            if with_position > 0:
                first_ac = next(ac for ac in aircraft if ac.get('lat') and ac.get('lon'))
                print(f"   ✈️  Örnek uçak:")
                print(f"      HEX: {first_ac.get('hex')}")
                print(f"      Flight: {first_ac.get('flight', 'N/A').strip()}")
                print(f"      Lat/Lon: {first_ac.get('lat')}, {first_ac.get('lon')}")
                print(f"      Alt: {first_ac.get('alt_baro') or first_ac.get('altitude', 'N/A')} ft")
                print(f"      Speed: {first_ac.get('gs') or first_ac.get('speed', 'N/A')} kts")
                print(f"      Track: {first_ac.get('track', 'N/A')}°")

            print()

            total_aircraft += with_position
            valid_files += 1

        except json.JSONDecodeError as e:
            print(f"❌ {json_file.name}: JSON parse hatası - {e}\n")
        except Exception as e:
            print(f"❌ {json_file.name}: Hata - {e}\n")

    print("=" * 50)
    print(f"📊 ÖZET:")
    print(f"   Geçerli dosya: {valid_files}/{len(json_files)}")
    print(f"   Toplam uçak (pozisyonlu): {total_aircraft}")
    print(f"   Ortalama uçak/dosya: {total_aircraft / valid_files if valid_files > 0 else 0:.1f}")
    print("=" * 50)

    if valid_files == 0:
        print("\n❌ Hiç geçerli JSON dosyası bulunamadı!")
        return False

    if total_aircraft == 0:
        print("\n⚠️  Hiçbir uçakta pozisyon bilgisi yok!")
        print("   JSON dosyalarınızda 'lat' ve 'lon' alanları olmalı.")
        return False

    print("\n✅ JSON dosyaları hazır! python app.py ile başlatabilirsiniz.")
    return True


if __name__ == '__main__':
    test_json_files()