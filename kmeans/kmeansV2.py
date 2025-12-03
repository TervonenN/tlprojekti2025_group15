import numpy as np
import matplotlib.pyplot as plt
import re

def read_data(file_path):
    data = []
    pattern = re.compile(r"x=(\d+), y=(\d+), z=(\d+)")
    with open(file_path, 'r') as f:
        for line in f:
            match = pattern.search(line)
            if match:
                data.append([float(x) for x in match. groups()])
    return np.array(data)

def kmeans_plus_init(data, k):
    centroids = [data[np.random.randint(len(data))]]
    for _ in range(1, k):
        dist = np.array([min([np.linalg.norm(x-c)**2 for c in centroids]) for x in data])
        centroids.append(data[np. random.choice(len(data), p=dist/dist.sum())])
    return np.array(centroids)

def kmeans(data, k=6):
    centroids = kmeans_plus_init(data, k)
    
    for _ in range(50):
        # pisteiden luokitus
        labels = np.array([np.argmin([np. linalg.norm(point-c) for c in centroids]) for point in data])
        
        # keskipisteiden päivitys
        new_centroids = np.array([data[labels==i].mean(axis=0) if np.sum(labels==i)>0 else centroids[i] for i in range(k)])
        
        if np.allclose(centroids, new_centroids, atol=0.1):
            break
        centroids = new_centroids
    
    return centroids, labels

def save_to_header(centroids, filename="keskipisteet.h"):
    with open(filename, 'w') as f:
        f.write("#ifndef KESKIPISTEET_H\n#define KESKIPISTEET_H\n\n")
        f.write(f"int CP[6][3] = {{\n")
        for i, c in enumerate(centroids):
            x, y, z = [int(round(coord)) for coord in c]
            f.write(f"    {{{x}, {y}, {z}}}")
            if i < 5: f.write(",")
            f.write(f" // Suunta {i+1}\n")
        f.write("};\n\n#endif\n")
    print(f"Tallennettu: {filename}")

def plot_results(data, centroids, labels):
    fig = plt.figure(figsize=(10,8))
    ax = fig. add_subplot(111, projection='3d')
    
    colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown']
    for i in range(6):
        cluster_data = data[labels==i]
        ax.scatter(cluster_data[:,0], cluster_data[:,1], cluster_data[:,2], c=colors[i], alpha=0.6)
    
    ax.scatter(centroids[:,0], centroids[:,1], centroids[:,2], c='black', marker='x', s=200)
    ax.set_xlabel('X'); ax.set_ylabel('Y'); ax.set_zlabel('Z')
    plt.show()

# Pääohjelma täällä
data = read_data("oikea_data.csv")
centroids, labels = kmeans(data)
print("Keskipisteet:")
for i, c in enumerate(centroids):
    print(f"Suunta {i+1}: X={c[0]:.1f}, Y={c[1]:.1f}, Z={c[2]:.1f}")
plot_results(data, centroids, labels)
save_to_header(centroids)