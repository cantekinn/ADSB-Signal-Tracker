#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Import kontrolü
"""

print("🔍 Import kontrol ediliyor...\n")

# 1. config.py
try:
    import config

    print("✅ config.py - OK")
    print(f"   USE_JSON_FILES: {config.USE_JSON_FILES}")
    print(f"   JSON_FILES_DIR: {config.JSON_FILES_DIR}")
except Exception as e:
    print(f"❌ config.py - HATA: {e}")

# 2. utils.py
try:
    from utils import debug_log, haversine_km

    print("✅ utils.py - OK")
    debug_log("Test mesajı")
except Exception as e:
    print(f"❌ utils.py - HATA: {e}")

# 3. position_validator.py
try:
    from position_validator import PositionValidator

    print("✅ position_validator.py - OK")
    validator = PositionValidator("test")
    print(f"   Test validator oluşturuldu: {validator.hex_id}")
except Exception as e:
    print(f"❌ position_validator.py - HATA: {e}")

# 4. json_reader.py
try:
    print("\n📖 json_reader.py kontrol ediliyor...")
    import json_reader

    # Modül içindeki tüm isimleri listele
    print(f"   Modüldeki isimler: {dir(json_reader)}")

    # get_json_reader var mı?
    if hasattr(json_reader, 'get_json_reader'):
        print("   ✅ get_json_reader fonksiyonu bulundu")
        reader = json_reader.get_json_reader()
        print(f"   ✅ Reader oluşturuldu: {len(reader.json_files)} dosya")
    else:
        print("   ❌ get_json_reader fonksiyonu BULUNAMADI!")
        print("   ℹ️  Dosyanın içeriği kontrol edilmeli")

except Exception as e:
    print(f"❌ json_reader.py - HATA: {e}")
    import traceback

    traceback.print_exc()

print("\n" + "=" * 50)
print("Kontrol tamamlandı!")