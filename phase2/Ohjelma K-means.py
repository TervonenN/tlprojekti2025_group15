# K-Means vaiheet
# 1. alustus
# 2. etäisyyden laskeminen ja määrittäminen
# 3. päivittäminen



import numpy as np
import matplotlib.pyplot as plt
import re


#####################
# lisäsin tämän tänne ylös, vaiheesta kolme
#####################
def update_centroids(number_of_clusters, np_data, clusters):
    new_centroids = np.zeros((number_of_clusters, np_data.shape[1]))
   
    for i in range(number_of_clusters):
        cluster_points = np_data[clusters == i]
       
        if len(cluster_points) > 0:
           new_centroids[i] = np.mean(cluster_points, axis=0)
        else:
            random_index = np.random.randint(0, len(np_data))
            new_centroids[i] = np_data[random_index]
            print(f"Klusteri {i} oli tyhjä -> arvottiin uusi centroidi:", new_centroids[i])
            
    return new_centroids
#####################


#############
## vaihe 1 ##
#############


data_points = []
    
#etsitään CSV-tiedostosta x,y ja z ja luodaan niistä ryhmä joista tietoa voidaan poimia

filepath = r'C:\KOULU\vuosi_2_periodi_2\Projekti\oikea_data.csv'
#filepath = r"oikea_data.csv"
# jos tiedoston luvussa tulee myöhemmin ongelmia, tarkasta tämä

xyzGroups = re.compile(r'x=(\d+), y=(\d+), z=(\d+)')

try:
    with open(filepath, 'r') as f:
        for line in f:
            #parsintaa tähän
            match = xyzGroups.search(line)
            if match:
                x_str = match.group(1)
                y_str = match.group(2)
                z_str = match.group(3)
                
                x = int(x_str)
                y = int(y_str)
                z = int(z_str)
                
                data_points.append([x, y, z])
         
            
except Exception as e:
    print("Error: datan luku ei onnistunut:#", {e}, " \n Tarkista filepath ")


np_data = np.array(data_points) #laitoin kaiken kerätyn datan np_data nimiseen muuttujaan,
                                #jotta siitä on helppo hakea erilaisia arvoja (min, max, mean)
print("minimiarvo: ", np.min(np_data)) # 1154
print("maksimiarvo: ", np.max(np_data)) # 1829

random_data = []

random_x = np.random.randint(np.min(np_data), np.max(np_data), size = 6)
random_y = np.random.randint(np.min(np_data), np.max(np_data), size = 6)
random_z = np.random.randint(np.min(np_data), np.max(np_data), size = 6)

random_data = np.stack((random_x, random_y, random_z), axis=1)

print("randomit: \n", random_data)

#############
## RULETTI ##
#############

all_centroids = random_data.shape[0]
max_rounds = 100
current_centroids = random_data # siirretään randomit currenteiksi niin saadaan ne mukavasti käyttöön


#############
## vaihe 2 ##
#############0

# tee for-loop joka tsekkaa cenrtoid-pointit ja vertaa jokaista pointtia kaikkiin data_pointteihin
# laske vertaa jokaista random_data jokaiseen data_pointsiin
# tallenna kaikki tulokset johonkin arrayhin ja etsi minimitulos
# julista pienin arvo voittajaksi
for rounds in range(max_rounds):
    clusters = []
    max_value = np.max(np_data)

    closest_data_centroid = 0

    old_centroids = current_centroids #siirrellään tän avulla centroideja lähemmäksi kohdetta
        
    for data_point_index, D_centroid_point in enumerate(np_data):
        
        min_distance = max_value #tässä voisi käyttää myös infinitiä, mutta laitoin maximin joka datasta löytyy
        closest_data_centroid = -1 #laitetaan -1 niin virheen sattuessa huomataan
        
            
        for R_centroid_index, R_centroid_point in enumerate(old_centroids): #vaihdoin sulkeisiin random_datan tilalle old_centroids jotta kierrättäminen toimii
            
            distance = np.linalg.norm(D_centroid_point - R_centroid_point)
            
            if distance < min_distance: #jos tämä etäisyys pienempi kuin pienin mahd. etäisyys
                min_distance = distance #päivitetään min_distance distanceksi ja 
                closest_data_centroid = R_centroid_index #closest_data_centroid R_centroid_indeksiksi
            
                
        clusters.append(closest_data_centroid)

    final_clusters = np.array(clusters) #muutetaan saadut tulokset numpy arrayksi, laitoin nimeksi final, jotta se on eri kuin pelkkä clusters
   
    current_centroids = update_centroids(all_centroids, np_data, final_clusters)

    if np.allclose(old_centroids,current_centroids, atol=1e-4):
        print("no nyt!")
        break

#############
## vaihe 3 ##
#############
# nyt pitäisi olla kuusi eri clusteria joihin on kaikkiin saatu jokin arvo, eli määrä kuinka
# usein mikäkin data-arvo oli lähinnä random-pistettä. Näiden arvojen yhteenlaskettu määrä
# pitäisi olla 200 koska 1200/6=200.

# clusteri on voinut saada vaikka kolme eri koordinaattia joiden x, y ja z tulokset lasketaan
# yhteen ja jaetaan kolmella jolloin saadaan kolme keskiarvoa joita käytetään uudella
# kierroksella taas määrittelyyn niin pitkään etteivät pallurat enää liiku

#current_centroids = update_centroids(all_centroids, np_data, clusters)
final_centroids = current_centroids
final_final_clusters = final_clusters


x = np.array(data_points)
y = final_centroids

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter(x[:,0], x[:,1], x[:,2],color='red')
ax.scatter(y[:,0], y[:,1], y[:,2],color='blue')

# Akselien nimet
ax.set_xlabel('X-akseli')
ax.set_ylabel('Y-akseli')
ax.set_zlabel('Z-akseli')

plt.show()