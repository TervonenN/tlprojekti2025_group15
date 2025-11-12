import requests

# Asetukset
groupid = 15
url = f"http://172.20.241.9/luedataa_kannasta_groupid_csv.php?groupid={groupid}"
tiedosto = "data.csv"

# Haetaan data HTTP GET -pyynnöllä
print(f"Haetaan dataa groupid={groupid}...")
response = requests.get(url)

# Tarkistetaan onnistuiko pyyntö
if response.status_code == 200:
    # Tallennetaan CSV-tiedostoksi
    with open(tiedosto, "w") as f:
        f.write(response.text)
    
    rivit = len(response.text.split('\n'))
    print(f"Valmis! Tallennettu {rivit} riviä tiedostoon {tiedosto}")
else:
    print(f"Virhe: HTTP {response.status_code}")