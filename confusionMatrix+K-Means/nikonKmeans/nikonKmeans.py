#  Tarvittavat kirjastot ja alkuasetukset
import numpy as np # käytetään tätä matemaattisiin operaatioihin ja taulukoiden käsittelyyn
from numpy.linalg import norm  # Euklidisen etäisyyden laskentaan
import matplotlib.pyplot as plt # Visualisointiin
from mpl_toolkits.mplot3d import Axes3D # 3D kuvia varten
import re # Lausekkeiden käsittelyyn
import sys # järjestelmätoiminnot

# Määritykset alla
FILE_NAME = "oikea_data.csv" # Tiedoston nimi, josta data haetaan
N_CLUSTERS = 6 # K-arvo = Klustereiden lukumäärä, joka tässä tarkoittaa yhtä suuntaa/asentoa joita meillä 6
MAX_ITERATIONS = 100 # Maksimi kierrosten määrä (iterointien määrä)
TOLERANCE = 0.01 # Lopetusehto, keskipisteet lopettaa siirtymisen kun liike on alle 0.01
# eli kun kun klusterit ovat vakiintuneet eivätkä enää juuri muutu
# Säästää laskenta-aikaa turhien kierrosten välttämiseksi

def calculate_distance(p1, p2):
    # laskee euklidisen etäisyyden kahden pisteen (mittaus vs keskipiste) välillä
    return np.linalg.norm(p1 - p2)

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
    # palautetaan data numpy-taulukkona
    return np.array(data)

# TÄSSÄ NYT NIKON "YLIMÄÄRÄISTÄ" VÄRKKÄILYÄ..testataan merin overkilliä vastaan
# tarkoituksena parantaa aloituskeskipisteiden valintaa kmeans++ menetelmällä jota scikit käyttää ilmeisesti automaationa
def kmeansplusplus(data, n_clusters):
    n_samples = data.shape[0]
    centroids = [] # kerätään tähän valitut centroidit

    # STEP 1: Valitaan ensimmäinen centroidi satunnaisesti
    print("Kmeans++..valitaan random ensimmäinen centroid")
    first_idx = np.random.randint(0, n_samples)
    centroids.append(data[first_idx].copy())
    print(f" Ensimmäiseksi centroidiks valikoitui: {first_idx}: {data[first_idx]}")

    # STEP 2: Tästä alaspäin taikaa tapahtuu
    for c in range(1, n_clusters):
        print(f"Kmeans++ valitaan centroidi {c+1}/{n_clusters}")

        # Lasketaan jokaisen pisteen etäisyys lähimpään centroidiin
        distances = np.zeros(n_samples)
        for i in range(n_samples):
            point = data[i]
            min_distance = float('inf')
            for centroid in centroids:
                dist = calculate_distance(point, centroid)
                if dist < min_distance:
                    min_distance = dist # päivitetään pienin etäisyys
            distances[i] = min_distance

            # STEP 3: Lasketaan todennäköisyydet: mitä kauempana piste on sitä todennäköisemmin valitaan
        probabilities = distances ** 2
        probabilities = probabilities / probabilities.sum()

            # STEP 4: Käytetään noita laskettuja todennäköisyyksiä uuden centroidin valintaan
        next_idx = np.random.choice(n_samples, p=probabilities)
        centroids.append(data[next_idx].copy())
        print(f"Valittu piste {next_idx}: {data[next_idx]}")
        print(f"Etäisyys lähimpään centroidiin: {distances[next_idx]:.1f}")
    
    return np.array(centroids)


# Vaihe 3: Toteutetaan K-means algoritmi
def kmeans(data, n_clusters=N_CLUSTERS, max_iterations=MAX_ITERATIONS, tolerance=TOLERANCE):
    numberOfRows = data.shape[0] # <- ulompi for luuppi kiertää 
   # alustus: satunnainen aloitus (arvotaan 6 keskipistettä datasta)
    centroids = kmeansplusplus(data, n_clusters)
# Alustetaan satunnaiset aloituskeskipisteet
# Valitaan 6 satunnaista riviä datasta klusterien aloituspisteiksi
# replace=False varmistaa ettei sama rivi tule kahdesti
# Määritetään keskipisteet (centroids) satunnaisten pisteiden arvoihin
    

    # PÄÄLUUPPI JOTA TOISTETAAN KUNNES VAKAA!
    for iteration in range(MAX_ITERATIONS):
        # Tähän muuttujaan summataan pisteiden arvot
        centerPointCumulativeSum = np.zeros((N_CLUSTERS, 3))
        # Kasvatetaan datapisteiden lukumäärää yhdellä
        counts = np.zeros(N_CLUSTERS, dtype=int)
        labels = np.zeros(numberOfRows, dtype=int)
        # Koko opetusdata käydään läpi
        # käsittelee jokaisen mittauspisteen (numberOfRows!)
        for i in range(numberOfRows):
            point = data[i]
            distances = np.zeros(N_CLUSTERS)
            # Lasketaan etäisyydet kaikkiin 6 keskipisteeseen
            for j in range(N_CLUSTERS):
                distances[j] = calculate_distance(point, centroids[j])
            
            # Selvitetään minkä keskipisteen etäisyys oli pienin
            nearest_cluster = np.argmin(distances) # palauttaa pienimmän etäisyyden indeksin
            labels[i] = nearest_cluster
            # päivitetään klusterin summapisteet ja laskuri
            centerPointCumulativeSum[nearest_cluster] += point
            # kasvatetaan laskuria yhdellä
            counts[nearest_cluster] += 1

            # Keskipisteiden päivitys
        new_centroids = np.zeros_like(centroids) # uusi taulukko päivitetyille arvoille

        for j in range(N_CLUSTERS):
            if counts[j] > 0:
                    # keskiarvo = summa / määrä = päivittyvä keskipiste
                new_centroids[j] = centerPointCumulativeSum[j] / counts[j]
            else:
                    # jos tyhjä klusteri, asetetaan satunnainen piste
                new_centroids[j] = data[np.random.choice(numberOfRows)]
            # Tässä tarkistetaan onko keskipisteiden liike alle toleranssin
            # eli "Euklidinen etäisyys", jos siirtymä on pientä = oppiminen vakaata
        movement = np.linalg.norm(new_centroids - centroids)
        centroids = new_centroids # päivitetään keskipisteet
            #return centroids, labels
        print(f"Iteraatio {iteration + 1}/{max_iterations}")
        print(f" Käsitelty {numberOfRows} pistettä")
        print(f" Klusterit: {counts}")
        print(f" Liike: {movement:.2f}")

        if movement < tolerance:
            print(f"Vakiintunut iteraatiolla {iteration + 1}")
            break
    
    return centroids, labels

def save_to_header(centroids, filename="keskipisteet.h"):
    with open(filename, 'w') as f:
        f.write("// Keskipisteet K-means klusteroinnista\n")  
        f. write("#ifndef KESKIPISTEET_H\n")                   
        f.write("#define KESKIPISTEET_H\n\n")                
        f.write(f"int CP[{N_CLUSTERS}][3] = {{\n")            

        for i, centroid in enumerate(centroids):
            x, y, z = [int(round(coord)) for coord in centroid]
            f.write(f"    {{{x}, {y}, {z}}}")                 
            if i < len(centroids) - 1:
                f.write(",")
            f.write(f" // Keskipiste {i+1}\n")
        
        f.write("};\n\n")                                      
        f.write("#endif // KESKIPISTEET_H\n")                
    
    print(f"Keskipisteet tallennettu tiedostoon: {filename}")
# 3D-visualisointi
def visualize_3d_result(data, centroids, labels):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Piirretään datapisteet klusterin värillä
    ax.scatter(data[:,0], data[:,1], data[:,2], c=labels, cmap='rainbow', alpha=0.6, s=10)

    # Piirretään keskipisteet (centroids) isoilla punasilla rasteilla
    ax.scatter(centroids[:,0], centroids[:,1], centroids[:,2], c='red', marker='X', s=200, label='Keskipisteet')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('K-means Klusterointi 3D-visualisointi')
    ax.legend()
    plt.show()

if __name__ == "__main__": 
    # luetaan data
    data = read_data(FILE_NAME)
    if data is None:
        sys.exit(1) # lopetetetaan jos ei löydy

    if data is not None:
        # Opetusdata löytyy, suoritetaan K-means
        final_centroids, labels = kmeans(data)

        # visualisoidaan tulokset 3D-kuvana
        visualize_3d_result(data, final_centroids, labels)

        # tallennetaan keskipisteet headeriin
        save_to_header(final_centroids)