import asyncio
from bleak import BleakScanner

async def main():
    print("Skannataan BLE-laitteita 10 sekunnin ajan...")
    print("Varmista etta Nordic-alustasi on paalla ja Bluetooth kaytossa!\n")
    
    try:
        devices = await BleakScanner.discover(timeout=10.0, return_adv=True)
        
        print(f"\nLoydettiin {len(devices)} BLE-laitetta:\n")
        print(f"{'Nimi':<30s} | {'MAC-osoite':<20s} | {'RSSI'}")
        print("-" * 70)
        
        for address, (device, adv_data) in devices.items():
            name = device.name if device.name else "(ei nimea)"
            rssi = adv_data.rssi
            print(f"{name:<30s} | {address:<20s} | {rssi} dBm")
        
        print("\nEtsi Nordic-alustasi nimi tai MAC-osoite listasta!")
        print("Kopioi MAC-osoite talteen seuraavaa vaihetta varten.\n")
        
    except Exception as e:
        print(f"Virhe: {e}")
        print("\nVarmista etta:")
        print("  1. Nordic-alusta on paalla")
        print("  2. Bluetooth on aktivoitu Nordic-koodissa")
        print("  3. Raspberry Pi:n Bluetooth on kaytossa")

if __name__ == "__main__":
    asyncio.run(main())
