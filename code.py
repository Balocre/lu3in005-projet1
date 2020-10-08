import random
import numpy as np
import matplotlib.pyplot as plt

#Constantes
N = 10
#Dictionnaire reliant les differents bateaux et leur taille en nombre de case
bateaux = dict() #dictionnaire de bateaux
bateaux = {1:5, 2:4, 3:3, 4:3, 5:2}

#Représentation du plateau vide en tant que matrice 10x10
plateau = np.zeros( (10,10) )

def peut_placer(grille,bateau,position,direction):
    """
    Teste s'il est possible de placer un bateau dans une direction souhaitee
    a la case position de la grille
    Args:
        grille (int[][]): r 2D 10x10
        bateau (String): nom du bateau
        position (int*int): position dans la matrice 
        direction (int): 1 pour horizontal, 2 pour vertical

    Returns:
        [type]: [boolean]
    """
    (k,l) = position
    if (k >= N or l >= N): return False
    if (direction == 1):
        if (l + bateaux[bateau] <= N):
            return np.array_equal(grille[k,l:l + bateaux[bateau]], np.zeros(bateaux[bateau],dtype=int))
    else :
        if (k + bateaux[bateau] <= N):
            return np.array_equal(grille[k:k + bateaux[bateau],l], np.zeros(bateaux[bateau],dtype=int))
    

def place(grille,bateau,position,direction):
    """
    Place un bateau si c'est possible et retourne True sinon retourne False
    Args:
        grille (int[][]): r 2D 10x10
        bateau (String): nom du bateau
        position (int*int): position dans la matrice 
        direction (int): 1 pour horizontal, 2 pour vertical
    """
    (k,l) = position
    i=k
    j=l
    if (peut_placer(grille,bateau,position,direction)):
        if (direction == 1):
            for j in range(l,l+bateaux[bateau]):
                grille[i][j]=bateau
        else :
            for i in range(k,k+bateaux[bateau]):
                grille[i][j]=bateau
        return True
    return False

def place_alea(grille,bateau):
    """
        Place un bateau de position et direction aleatoire dans la grille
    Args:
        grille (int[][]): r 2D 10x10
        bateau (String): nom du bateau
    """
    b=False
    while not b:
        position = (random.randint(0,9),random.randint(0,9))
        direction = random.randint(1,2)
        b = place(grille,bateau,position,direction)
    return b


def affiche(grille):
    """Affiche l'état de la grille à l'aide de la librairie matplotlib"""
    plt.matshow(grille)
    plt.show()

def eq(grille_a, grille_b):
    """Compare 2 grilles et renvoie 1 si elles sont égales, 0 sinon, -1 si les grille ne sont pas comparables"""
    row_a = len(grille_a)
    col_a = len(grille_a[0])

    row_b = len(grille_b)
    col_b = len(grille_b[0])

    if( (row_a != row_b) or (col_a != col_b) ):
        return -1

    if np.array_equal(grille_a, grille_b):
        return 1

    return 0
    
def genere_grille():
    grille = np.zeros( (10, 10) )
    for b in range(1, 5):
        place_alea(grille, b)
    return grille

#Partie 2

def nb_pos(grille,bateau):
    """
    Compte le nombre de facons de placer un bateau dans la grille
    Args:
        grille (int[][]): r 2D 10x10
        bateau (String): nom du bateau
    """
    cpt = 0
    for i in range(N):
        for j in range(N):
            if (peut_placer(grille,bateau,(i,j),1)):
                cpt+=1
            if (peut_placer(grille,bateau,(i,j),2)):
                cpt+=1
    return cpt

def nb_pos_list(grille,L):
    if not L : return 0
    if len(L)==1 : return nb_pos(grille,L[0])
    else :
        cpt = 0
        for i in range(N):
            for j in range(N):
                g1 = np.copy(grille)
                if place(g1,L[0],(i,j),1): cpt = cpt + nb_pos_list(g1,L[1:])
                g2 = np.copy(grille)
                if place(g2,L[0],(i,j),2): cpt = cpt + nb_pos_list(g2,L[1:])
        return cpt

def comp_alea_grille(grille):
    i = 0
    do
    {
        r = eq(grille, genere_grille())
        i+=1
        print("r={}".format(r))
    } while (r !=  1)
    return i

def approx_total_grilles(n):
    r = np.array([])
    g = genere_grille()
    for i in range(n):
        np.append(r, comp_alea_grille(g))

    return np.average(r)