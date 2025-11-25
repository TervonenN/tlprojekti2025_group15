# Vaihe 1 : Tarvittavat kirjastot ja alkuasetukset
import numpy as np # käytetään tätä matemaattisiin operaatioihin ja taulukoiden käsittelyyn
from numpy.linalg import norm  # Euklidisen etäisyyden laskentaan
import re # Lausekkeiden käsittelyyn?
import sys # järjestelmätoiminnot

# Määritykset alla
FILE_NAME = "oikea_data.csv" # Tiedoston nimi, josta data haetaan
N_CLUSTERS = 6 # K-arvo = Klustereiden lukumäärä, joka tässä tarkoittaa yhtä suuntaa/asentoa joita meillä 6
MAX_ITERATIONS = 100 # Maksimi kierrosten määrä (iterointien määrä)
TOLERANCE = 1.0 # Lopetusehto, keskipisteet lopettaa siirtymisen kun liike on alle 1.0
# eli kun kun klusterit ovat vakiintuneet eivätkä enää juuri muutu
# Säästää laskenta-aikaa turhien kierrosten välttämiseksi

# Vaihe 2 : Datan lukeminen

# Lukee ADC-mittausdatan (X Y Z) CSV-tiedostosta ja palauttaa sen NumPy-taulukkona
def read_data(file_path):
    print(f"Luetaan dataa tiedostosta: {file_path}")
    # Tällä poimitaan numerot X, Y, Z arvoista
    pattern = re.compile(r"Suunta=\d+, x=(\d+), y=(\d+), z=(\d+)")
    data = []

    try:
        with open(file_path, 'r') as f:
            for line in f:
                match = pattern.search(line)
                if match:
                    # tässä muutos stringit -> floateiksi laskentaa varten
                    x, y, z = map(int, match.groups())
                    data.append([float(x), float(y), float(z)])
    except FileNotFoundError:
        print(f"\nVirhe: Tiedostoa '{file_path}' ei löytynyt. Varmista että tiedosto on samassa kansiossa!")
        return None
    print(f"Dataa löytyi {len(data)} riviä")
    return np.array(data)

# Vaihe 3: Toteutetaan K-means algoritmi
def kmeans(data, n_clusters, max_iterations, tolerance):
    
    n_samples, n_features = data.shape # n_samples = rivien määrä, n_features = sarakkeiden määrä eli 3

    # Alustetaan satunnaiset aloituskeskipisteet (centroids?)
    # Valitaan 6 satunnaista riviä datasta klusterien aloituspisteiksi
    # replace=False varmistaa ettei sama rivi tule kahdesti
    random_indices = np.random.choice(n_samples, n_clusters, replace=False) 
    # Määritetään keskipisteet (centroids) satunnaisten pisteiden arvoihin

if __name__ == "__main__":
    # luetaan data
    data = read_data(FILE_NAME)
    if data is None:
        sys.exit(1) # lopetetetaan jos ei löydy (ja sitähän löytyi :D)