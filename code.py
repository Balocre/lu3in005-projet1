import random
import numpy as np
import matplotlib.pyplot as plt
import itertools as itr

#Constantes
N = 10
#Dictionnaire reliant les differents bateaux et leur taille en nombre de case
bateaux = dict() #dictionnaire de bateaux
bateaux = {1:5, 2:4, 3:3, 4:3, 5:2}

#Représentation du plateau vide en tant que matrice 10x10
plateau = np.zeros( (10,10) )

# Partie 1

def peut_placer(grille, id_bat, position, direction):
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
    # version explitant numpy un peu mieux
    #taille_bat = bateaux[id_bat]
    #if (k < 0 or l < 0 or k + taille_bat >= N or l + taille_bat): return False # on vérifie que les coordonées sont dans la grille
    #if (direction == 1): # horizontale vers la droite
    #    if not np.all(grille[k, l:l+taille_bat]): return True # on vérifie que les cases de la grille sont libres
    #elif (direction == 2): # verticale vers le bas
    #    if not np.all(grille[k:k+taille_bat, l]): return True 

    if (k >= N or l >= N): return False # on test voir si la position est dans la grille
    if (direction == 1):
        if (l + bateaux[id_bat] <= N):
            return np.array_equal(grille[k,l:l + bateaux[id_bat]], np.zeros(bateaux[id_bat], dtype=int))
    else :
        if (k + bateaux[id_bat] <= N):
            return np.array_equal(grille[k:k + bateaux[id_bat],l], np.zeros(bateaux[id_bat], dtype=int))
    

def place(grille, bateau, position, direction):
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
    if (peut_placer(grille, bateau, position, direction)):
        if (direction == 1):
            for j in range(l, l+bateaux[bateau]):
                grille[i][j] = bateau
        elif (direction == 2):
            for i in range(k, k+bateaux[bateau]):
                grille[i][j] = bateau
        else:
            return False
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
    plt.waitforbuttonpress()
    plt.close()

def eq(grille_a, grille_b):
    """Compare 2 grilles et renvoie 1 si elles sont égales, 0 sinon, -1 si les grille ne sont pas comparables"""
    row_a = len(grille_a)
    col_a = len(grille_a[0])

    row_b = len(grille_b)
    col_b = len(grille_b[0])

    if( (row_a != row_b) or (col_a != col_b) ): # si les matrices ne sont pas de tailel égale
        raise ValueError("Les matrices ne sont pas de même taille")

    if np.array_equal(grille_a, grille_b):
        return True

    return False
    
def genere_grille():
    grille = np.zeros( (10, 10) )
    for b in range(1, 5):
        place_alea(grille, b)
    return grille

# Partie 2

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
    while True:
        g = genere_grille()
        r = eq(grille, g)
        affiche(grille)
        affiche(g)
        i+=1
        # debug
        print("i={} r={}".format(i, r))
        if (r ==  1):
            break
    return i

def approx_total_grilles(n):
    r = np.array([])
    g = genere_grille()
    for i in range(n):
        np.append(r, comp_alea_grille(g))

    return np.average(r)


# Partie 3

class Bataille:

    def __init__(self):
        self.grille = genere_grille()

        self.carte_coups = np.zeros( (10, 10) )

        self.liste_touche = []

    def joue(self, position):
        (x, y) = position
        if self.grille[x, y]:
            self.carte_coups[x, y] = self.grille[x, y]
            return True
        return False

    def victoire(self):
        if eq(self.grille, self.carte_coups):
            return True
        return False

    def reset(self):
        pass
    
class Joueur:

    def __init__(self, bataille):
        self.bataille = bataille

    def joue(self):
        pass

class JoueurAlea(Joueur):

    def __init__(self, bataille):
        Joueur.__init__(self, bataille)
        
        # génère une liste de position aléatoires dans la grille
        self.liste_coups = itr.product(range(10), range(10)) 
        random.shuffle(self.liste_coups)

    def joue(self):
        pos = self.bataille.liste_coups.pop() # on sort la poisition jouée de la liste por ne pas répéter 2 fois un coup inutilement
        self.bataille.joue(pos)
    
class JoueurHeur(JoueurAlea): # hérite de joueur aléa, car le comportement par défaut est aléatoire

    def joue(self, pos=None, axe=None, direction=None):
        
        if not pos: # si pas de position passée joue une case aléatoirement
            pos = self.bataille.liste_coups.pop()
        
        if self.bataille.joue(pos): # si ce coup touche teste les cases avoisinantes avec un appel récursif de la fonction
            (x, y) = pos
            if (axe == 'x'):

                if ( direction != '-' and (x+1) < 10 ): # si ce coup fait suite à un coup joué dans la direction - on reseterait la mm case -> boucle infinie 
                    self.joue( (x+1, y), 'x', '+' )

                if ( direction != '+' and (x-1)  >= 0 ):
                    self.joue( (x-1, y) )

            elif (axe == 'y'):

                if ( direction != '-' and (y+1) < 10 ):
                    self.joue( (x, y+1) )

                if ( direction != '+' and (y-1)  >= 0 ):
                    self.joue( (x, y-1) )

            else: # si pas d'axe ni de direction rejoue le même coup avec axe et dir choisis aléatoirement
                self.joue(pos, random.choice(['x', 'y']), random.choice(['-', '+']))

class JoueurProba:
