import asyncio
from bleak import BleakClient
import mysql.connector

# ===== ASETUKSET =====

# MySQL-palvelimen tiedot
DB_HOST = '172.20.241.9'
DB_USER = 'dbaccess_rw'
DB_PASSWORD = 'fasdjkf2389vw2c3k234vk2f3'
DB_NAME = 'measurements'

# Nordic-alustan tiedot
NORDIC_MAC = "C4:0B:6E:44:7A:02"
GROUP_ID = 15

# BLE Characteristic UUID (paivita kun tiedossa)
CHAR_UUID = "00001526-1212-efde-1523-785feabcd123"


# ===== FUNKTIOT =====

def tallenna_kantaan(sensor_a, sensor_b, sensor_c):
    """
    Tallentaa anturidata tietokantaan.
    Parametrit: kolme sensoriarvoa (float)
    Palauttaa: True jos onnistui, False jos epaonnistui
    """
    try:
        # Yhdista tietokantaan
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()
        
        # SQL-kysely datan lisaamiseen
        query = """
        INSERT INTO rawdata 
        (groupid, from_mac, to_mac, sensorvalue_a, sensorvalue_b, sensorvalue_c) 
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        # Suorita kysely
        cursor.execute(query, (GROUP_ID, NORDIC_MAC, "RaspberryPi", sensor_a, sensor_b, sensor_c))
        conn.commit()
        
        # Sulje yhteys
        cursor.close()
        conn.close()
        
        print(f"OK: Tallennettu A={sensor_a}, B={sensor_b}, C={sensor_c}")
        return True
        
    except Exception as e:
        print(f"VIRHE tallennuksessa: {e}")
        return False


async def listaa_servicet():
    """
    Yhdistaa Nordic-alustaan ja listaa kaikki BLE-servicet.
    Tasta naet mita UUID:ita kaytettavissa.
    """
    print(f"Yhdistetaan: {NORDIC_MAC}")
    
    async with BleakClient(NORDIC_MAC) as client:
        print("Yhdistetty!\n")
        
        # Kayn lapi kaikki servicet
        for service in client.services:
            print(f"SERVICE: {service.uuid}")
            
            # Kayn lapi servicen characteristicit
            for char in service.characteristics:
                print(f"  CHAR: {char.uuid} ({', '.join(char.properties)})")
            print()

async def lue_ja_tallenna():
    """
    Yhdistaa Nordic-alustaan ja kuuntelee notify-ilmoituksia.
    Keraa 4 perakkaista arvoa ja tallentaa ne kantaan.
    """
    print(f"Yhdistetaan: {NORDIC_MAC}")
    
    received_data = []
    
    def notification_handler(sender, data):
        """Kutsutaan kun uutta dataa saapuu"""
        import struct
        if len(data) == 4:
            value = struct.unpack('<I', data)[0]
            print(f"Saapui arvo: {value}")
            received_data.append(value)
    
    client = BleakClient(NORDIC_MAC)
    
    try:
        await client.connect()
        print("Yhdistetty!")
        print("Kuunnellaan dataa 15 sekunnin ajan...\n")
        
        await client.start_notify(CHAR_UUID, notification_handler)
        await asyncio.sleep(15)
        
        try:
            await client.stop_notify(CHAR_UUID)
        except:
            pass
        
        if len(received_data) >= 4:
            print(f"\nSaatiin yhteensa {len(received_data)} arvoa")
            
            non_zero = [x for x in received_data if x != 0]
            
            if len(non_zero) >= 3:
                sensor_a = float(non_zero[-3])
                sensor_b = float(non_zero[-2])
                sensor_c = float(non_zero[-1])
                
                print(f"Tallennetaan: A={sensor_a}, B={sensor_b}, C={sensor_c}")
                tallenna_kantaan(sensor_a, sensor_b, sensor_c)
            else:
                print("Ei tarpeeksi ei-nolla arvoja")
        else:
            print("\nEi saatu tarpeeksi dataa!")
            
    except Exception as e:
        print(f"Virhe: {e}")
    finally:
        try:
            if client.is_connected:
                await client.disconnect()
        except:
            pass
        print("Yhteys suljettu")
# ===== PAAOHJELMA =====

async def main():
    print("BLE -> MySQL (Group 15)")
    print("-" * 40)
    print("1 = Listaa servicet/characteristicit")
    print("2 = Lue data ja tallenna kantaan")
    
    valinta = input("\nValitse: ")
    
    if valinta == "1":
        await listaa_servicet()
    elif valinta == "2":
        await lue_ja_tallenna()
    else:
        print("Virheellinen valinta")


if __name__ == "__main__":
    asyncio.run(main())
