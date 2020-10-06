import random
import numpy as np 

#Constantes
N=10
#Dictionnaire reliant les differents bateaux et leur taille en nombre de case
dict_bateau = dict() #dictionnaire de bateaux
dict_bateau = {1:5, 2:4,3:3,4:3,5:2}

#Fonction qui génère une grille vide
def grille_vide():
    """Genere une grille vide de dimension N*N """
    return np.zeros(shape=(N,N),dtype = int)


def peut_placer(grille,bateau,position,direction):
    """
    Teste s'il est possible de placer un bateau dans une direction souhaitee
    a la case position de la grille
    Args:
        grille (int[][]): map 2D 10x10
        bateau (String): nom du bateau
        position (int*int): position dans la matrice 
        direction (int): 1 pour horizontal, 2 pour vertical

    Returns:
        [type]: [boolean]
    """
    (k,l) = position
    if (k >= N or l >= N): return False
    if (direction == 1):
        if (l + dict_bateau[bateau] <= N):
            return np.array_equal(grille[k,l:l + dict_bateau[bateau]], np.zeros(dict_bateau[bateau],dtype=int))
    else :
        if (k + dict_bateau[bateau] <= N):
            return np.array_equal(grille[k:k + dict_bateau[bateau],l], np.zeros(dict_bateau[bateau],dtype=int))
    

def place(grille,bateau,position,direction):
    """
    Place un bateau si c'est possible et retourne True sinon retourne False
    Args:
        grille (int[][]): map 2D 10x10
        bateau (String): nom du bateau
        position (int*int): position dans la matrice 
        direction (int): 1 pour horizontal, 2 pour vertical
    """
    (k,l) = position
    i=k
    j=l
    if (peut_placer(grille,bateau,position,direction)):
        if (direction == 1):
            for j in range(l,l+dict_bateau[bateau]):
                grille[i][j]=bateau
        else :
            for i in range(k,k+dict_bateau[bateau]):
                grille[i][j]=bateau
        return True
    return False

def place_alea(grille,bateau):
    """
        Place un bateau de position et direction aleatoire dans la grille
    Args:
        grille (int[][]): map 2D 10x10
        bateau (String): nom du bateau
    """
    b=False
    while not b:
        position = (random.randint(0,9),random.randint(0,9))
        direction = random.randint(1,2)
        b = place(grille,bateau,position,direction)
    return b

#test
map = grille_vide()
place(map,1,(0,5),1)
place_alea(map,3)
place_alea(map,3)
place_alea(map,3)
print(map)

#Partie 2

def nb_pos(grille,bateau):
    """
    Compte le nombre de facons de placer un bateau dans la grille
    Args:
        grille (int[][]): map 2D 10x10
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

#Test nb_pos
grille = grille_vide()
print(nb_pos(grille,1))


def nb_pos_list(grille,L):
    if not L : return 0
    if len(L)==1 : return nb_pos(grille,L[0])
    else :
        cpt = 0
        for i in range(N):
            for j in range(N):
                g1 = np.copy(grille)
                if place(g1,L[0],(i,j),1):  cpt = cpt +  nb_pos_list(g1,L[1:])
                g2 = np.copy(grille)
                if place(g2,L[0],(i,j),2): cpt = cpt + nb_pos_list(g2,L[1:])
        return cpt

#Test nb_pos_list
print(nb_pos_list(grille,[1,1]))