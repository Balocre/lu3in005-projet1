import matplotlib.pyplot as plt
import numpy as np
from code.py import place_alea

def affiche(grille):
    plt.matshow(grille)
    plt.show()

def eq(grille_a, grille_b):
    row = len(grille_a)
    col = len(grille_a[0])

    for i in range(row):
        for j in range(col):
            if grille_a[i][j] != grille_b[i][j]:
                return 0

def genere(grille):
    grille = np.zeroes( (10, 10) )
    for b in range(5):
        place_alea(grille, b)
    
    return grille

aa = np.zeros((10, 10))
for i in range(10):
        aa[i, i] = i

plt.matshow(aa)
plt.show()