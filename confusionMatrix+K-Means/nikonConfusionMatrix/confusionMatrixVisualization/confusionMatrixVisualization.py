import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Tähän se confusion matrix tulos

confusion = np.array([
    [99, 1, 0, 0, 0, 0],   # Suunta 0 (cp1)
    [0, 99, 1, 0, 0, 0],   # Suunta 1 (cp2)
    [0, 0, 99, 1, 0, 0],   # Suunta 2 (cp3)
    [0, 0, 0, 99, 1, 0],   # Suunta 3 (cp4)
    [0, 0, 0, 0, 99, 1],   # Suunta 4 (cp5)
    [1, 0, 0, 0, 0, 99]    # Suunta 5 (cp6)
])

labels = ['CP0', 'CP1', 'CP2', 'CP3', 'CP4', 'CP5']

accuracy = np.trace(confusion) / np.sum(confusion) * 100
correct = np.trace(confusion)
total = np.sum(confusion)

print(f"Tarkkuus: {accuracy:.1f}% ({correct}/{total})")

plt.figure(figsize=(10, 8))
sns.heatmap(
    confusion,
    annot=True,
    fmt='d',
    cmap='Blues',
    xticklabels=labels,
    yticklabels=labels,
    cbar_kws={'label': 'Mittausten määrä'},
    linewidths=0.5,
    linecolor='gray'
)
plt.xlabel('Ennustettu suunta')
plt.ylabel('Todellinen suunta')
plt.title(f'K-means - Confusion Matrix\n Tarkkuus: {accuracy:.1f}%',
          fontsize=15, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('confusion_matrix.png', dpi=150, bbox_inches='tight')
print("Kuva tallennettu!")
plt.show()