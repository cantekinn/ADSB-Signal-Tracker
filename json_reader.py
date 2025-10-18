# json_reader.py
import json
import time
from pathlib import Path
from typing import List, Dict, Optional
import config
from utils import debug_log


class JSONDataReader:
    """JSON dosyalarından ADS-B verilerini okur"""

    def __init__(self, json_dir: Path):
        self.json_dir = json_dir
        self.json_files = []
        self.current_index = 0
        self.load_json_files()

    def load_json_files(self):
        """JSON dosyalarını listele ve sırala"""
        if not self.json_dir.exists():
            debug_log(f"❌ JSON dizini bulunamadı: {self.json_dir}", "ERROR")
            return

        # Tüm .json dosyalarını bul
        files = list(self.json_dir.glob("adsb_data_*.json"))

        if not files:
            debug_log("❌ JSON dosyası bulunamadı!", "ERROR")
            return

        # Dosyaları sayısal olarak sırala (adsb_data_X.json formatı için)
        def extract_number(filepath):
            """Dosya adından sayıyı çıkar"""
            try:
                # adsb_data_105.json -> 105
                name = filepath.stem  # adsb_data_105
                parts = name.split('_')  # ['adsb', 'data', '105']
                return int(parts[-1])  # 105
            except (ValueError, IndexError):
                return 0

        self.json_files = sorted(files, key=extract_number)
        debug_log(f"✅ {len(self.json_files)} JSON dosyası bulundu")

        # İlk 5 dosyayı göster
        for i, f in enumerate(self.json_files[:5]):
            debug_log(f"   📄 {f.name}")
        if len(self.json_files) > 5:
            debug_log(f"   ... ve {len(self.json_files) - 5} dosya daha")

    def read_next_data(self) -> Optional[Dict]:
        """Sıradaki JSON dosyasını oku"""
        if not self.json_files:
            debug_log("❌ Okunacak dosya yok", "ERROR")
            return None

        current_file = self.json_files[self.current_index]

        try:
            with open(current_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            aircraft_count = len(data.get('aircraft', []))
            debug_log(f"📖 Dosya okundu: {current_file.name} ({aircraft_count} uçak)")

            # Sıradaki dosyaya geç
            self.current_index += 1

            # Döngü kontrolü
            if self.current_index >= len(self.json_files):
                if config.JSON_LOOP:
                    debug_log("🔄 JSON dosyaları başa sarıldı")
                    self.current_index = 0
                else:
                    debug_log("⏹️ Tüm JSON dosyaları okundu")
                    return None

            return data

        except json.JSONDecodeError as e:
            debug_log(f"❌ JSON parse hatası ({current_file.name}): {e}", "ERROR")
            self.current_index += 1
            # Bir sonraki dosyayı dene
            if self.current_index < len(self.json_files):
                return self.read_next_data()
            return None

        except Exception as e:
            debug_log(f"❌ Dosya okuma hatası ({current_file.name}): {e}", "ERROR")
            self.current_index += 1
            return None

    def get_progress(self) -> Dict:
        """İlerleme bilgisi"""
        if not self.json_files:
            return {"current": 0, "total": 0, "percent": 0}

        return {
            "current": self.current_index,
            "total": len(self.json_files),
            "percent": (self.current_index / len(self.json_files)) * 100 if self.json_files else 0
        }

    def reset(self):
        """Başa sar"""
        self.current_index = 0
        debug_log("🔄 JSON okuyucu sıfırlandı")


# Singleton instance
_json_reader = None


def get_json_reader() -> JSONDataReader:
    """Global JSON okuyucu instance'ını döndür"""
    global _json_reader
    if _json_reader is None:
        _json_reader = JSONDataReader(config.JSON_FILES_DIR)
    return _json_reader