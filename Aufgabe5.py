import psutil
import time
from datetime import datetime
from pymongo import MongoClient
import os

class Power:
    def __init__(self, cpu=None, ram_total=None, ram_used=None, timestamp=None):
        if cpu is None or ram_total is None or ram_used is None or timestamp is None:
            self.cpu = psutil.cpu_percent(interval=1)
            virtual_mem = psutil.virtual_memory()
            self.ram_total = virtual_mem.total
            self.ram_used = virtual_mem.used
            self.timestamp = datetime.now()
        else:
            self.cpu = cpu
            self.ram_total = ram_total
            self.ram_used = ram_used
            self.timestamp = timestamp

    def to_dict(self):
        return {
            "cpu_percent": self.cpu,
            "ram_total": self.ram_total,
            "ram_used": self.ram_used,
            "timestamp": self.timestamp
        }

def main():
    uri = os.getenv("MONGO_URI")
    if not uri:
        print("Fehler: Umgebungsvariable MONGO_URI ist nicht gesetzt.")
        return

    client = MongoClient(uri)
    db = client["system_monitor"]
    collection = db["power_stats"]

    print("Starte Power-Statistik-Logger (Drücke Strg+C zum Beenden)...")

    try:
        while True:
            power = Power()
            collection.insert_one(power.to_dict())
            print(f"[{power.timestamp}] CPU: {power.cpu}% | RAM used: {power.ram_used / 1e9:.2f} GB / {power.ram_total / 1e9:.2f} GB")
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nLogger wurde beendet.")

if __name__ == "__main__":
    main()
