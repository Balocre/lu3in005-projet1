import random
import numpy as np
import matplotlib.pyplot as plt
import itertools as itr
import warnings
from typing import Optional
import math
from collections import OrderedDict
import sortedcontainers
from sortedcontainers import SortedDict


#Constantes
N = 10
#Dictionnaire reliant les differents bateaux et leur taille en nombre de case
bateaux = dict() #dictionnaire de bateaux
bateaux = {1:5, 2:4, 3:3, 4:3, 5:2}

#Représentation du plateau vide en tant que matrice 10x10
plateau = np.zeros( (10,10) )

# Partie 1

def peut_placer(grille, id_bat, pos, direction):
    """
    Teste s'il est possible de placer un bateau dans une direction souhaitee a la position pos de la grille.

    Args:
        grille (int[][]): Matrice représentant la grille de jeu.
        bateau (String): Nom du bateau.
        position (int*int): Position de l'origine du bateau dans la matrice.
        direction (String): Direction en fonctions des axes x (vertical) et y (horisontal) \"+x\" pour horizontal-droite, \"+y\" pour vertical-bas.

    Returns:
        bool: True si le bateau peut être placé, False sinon.
    """

    directions = set("+x", "+y")
    if direction not in directions: raise ValueError("{} n'est pas une direction valide".format(dir))

    (x, y) = pos
    taille_bat = bateaux[id_bat]

    if (x < 0) or (y < 0) or (x + taille_bat >= N) or (y + taille_bat >= N): return False # on vérifie que les coordonées sont dans la grille

    if (direction == "+y"): # horizontale vers la droite
       if not np.all(grille[x, y:y+taille_bat]): return True # on vérifie que les cases de la grille sont libres
    elif (direction == "+x"): # verticale vers le bas
       if not np.all(grille[x:x+taille_bat, y]): return True
    
    return False

def place(grille, id_bat, pos, direction) -> Optional[tuple(tuple())]:
    """
    Place un bateau si c'est possible et renvoie un tuple de coordonées correspondant à la position des pièces du bateau dans la grille ne renvoie None sinon.

    Args:
        grille (int[][]): r 2D 10x10
        bateau (String): nom du bateau
        position (int*int): position dans la matrice 
        direction (int): 1 pour horizontal, 2 pour vertical

    Returns:
        Optional[tuple(tuple())]
    """
    (x, y) = pos
    taille_bat = bateaux[id_bat]

    if not peut_placer(grille, id_bat, pos, direction): 
        return None
    
    else:
        if (direction == "+y"): 
            grille[x, y:y+taille_bat] = id_bat
            return tuple( (x, j) for j in range(y, y+taille_bat) )

        elif (direction == "+x"):
            grille[x:x+taille_bat, y] = id_bat
            return tuple( (i, y) for i in range(x, x+taille_bat) )


def place_alea(grille,bateau):
    """
        Place un bateau de position et direction aleatoire dans la grille
    Args:
        grille (int[][]): r 2D 10x10
        bateau (String): nom du bateau
    """

    while r := not place(grille, 
        bateau, 
        random.randint(0, 9, 2), 
        random.choice( set("+x", "+y")) 
        ):
        continue

    return r


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
        warnings.warn("Les matrices ne sont pas de la même taille")

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

        # XXX: peut-etre passer en np.empty? si pas de pb lors de la comparaison
        self.grille_decouverte = np.zeros( (10, 10) )

        self.liste_touche = []

        self.liste_coups = []

    def joue(self, pos) -> Optional[int]:
        self.liste_coups.append(pos)
        self.grille_decouverte[pos] = self.grille[pos] # on met à jour la carte de découverte
        if self.grille[pos]: # si il y a un bateau ou le joueur vise
            self.liste_touche.append(pos)
            return self.grille[pos] # la fonction renvoie l'id du bateau touché
        return None # la fonction indique que rien n'a été touché

    def victoire(self):
        if eq(self.grille, self.grille_decouverte):
            return True
        return False

    def reset(self):
        pass
    
class Joueur:

    def __init__(self, bataille):
        self.bataille = bataille

        self.coups_prep = None

    def joue(self):
        pass

class JoueurAlea(Joueur):

    def __init__(self, bataille):
        Joueur.__init__(self, bataille)
        
        # génère une liste de position aléatoires dans la grille
        self.coups_prep = itr.product(range(10), range(10)) 
        random.shuffle(self.coups_prep)

    def joue(self):
        pos = self.bataille.coups_prep.pop() # on pop la position jouée de la liste por ne pas répéter 2 fois un coup inutilement
        self.bataille.joue(pos)
    
class JoueurHeur(JoueurAlea): # hérite de joueur aléa, car le comportement par défaut est aléatoire

    def __init__(self, bataille):
        JoueurAlea.__init__(self, bataille)

        # XXX: utiliser un tuple comme valeur serait certainement plus rapide, dans ce cas corriger les index
        self.coups_prep = OrderedDict([(i, dict.fromkeys(bateaux.keys, 1)) for i in self.liste_coups]) # ce dictionnaire contient la liste des coups préparés par le joueur, en utilisant pour clé le couple (x, y) représentant la position du coup et ayant pour valeur un dict ayant pour clé les id des bateaux et valeur 1 si on peut trouver le bateau correspondant à la position 0 sinon 
        self.coups_joue = OrderedDict() # ce dict contient la liste des coups joués, en utilisant pour clé le couple (x, y) représentant la position du coup et ayant pour valeur l'id du bateau trouvé à la position ou None

    # TODO: 
    # traiter l'épuisement des cases
    def joue(self):

        (x, y) = self.bataille.liste_coups.popitem()
        b = self.bataille.joue( (x, y) ) # si le coup touche
        if b:
            # on retire la possibilité de trouver b aux positions potentielles "plus loin" qu'une position ayant déjà étée jouée avec un autre bateau que b ait été découvert ou dont on à éliminé la possibilité de contenir b
            for (i, y) in [(i, y) for i in range(x-1, x-bateaux[b], -1) if ( ( (i, y) in self.coups_prep and not self.coups_prep[(i, y)][b] ) or ( (i, y) in self.coups_joue and self.coups_joue[(i, y)] != b ))]: # pour les positions n'ayant pas été jouées et ne pouvant pas contenir b et les position ayant été jouées et contenant un autre bateau que b
                for (k, y) in [(k, y) for k in range(0, i) if (k, y) in self.coups_prep]: # pour les positions au-dessus d'une position matchée par l'expression ci-dessus
                    self.coups_prep[(i, y)][b] = 0 # on passe la valeur associée à la clé b à 0
            for (i, y) in [(i, y) for i in range(x+1, x+bateaux[b]) if ( ( (i, y) in self.coups_prep and not self.coups_prep[(i, y)][b] ) or ( (i, y) in self.coups_joue and self.coups_joue[(i, y)] != b ))]:
                for (k, y) in [(k, y) for k in range(10, i, -1) if (k, y) in self.coups_prep]:
                    self.coups_prep[(i, y)][b] = 0
            for (x, j) in [(x, j) for j in range(y+1, y+bateaux[b]) if ( ( (x, j) in self.coups_prep and not self.coups_prep[(x, j)][b] ) or ( (x, j) in self.coups_joue and self.coups_joue[(x, j)] != b ))]:
                for (x, l) in [(x, l) for l in range(10, i, -1) if (x, l) in self.coups_prep]:
                    self.coups_prep[(x, l)][b] = 0
            for (x, j) in [(x, j) for j in range(y-1, y-bateaux[b], -1) if ( ( (x, j) in self.coups_prep and not self.coups_prep[(x, j)][b] ) or ( (x, j) in self.coups_joue and self.coups_joue[(x, j)] != b ))]:
                for (x, l) in [(x, l) for l in range(0, i) if (x, l) in self.coups_prep]:
                    self.coups_prep[(x, l)][b] = 0
            

            # on augemnte la priorité des coups sur les positions pouvant potentiellement contenir le bateau b i.e. une croix autours de la position du b touché
            for c in itr.chain( # on itère sur des générateurs décrivant ces positions
                    # XXX: peu se faire avec une compréhension de liste
                    ((i, y) for i in range(x-1, x-bateaux[b]-1, -1) if (i, y) in self.coups_prep and self.coups_prep[(i, y)][b]),
                    ((i, y) for i in range(x+1, x+bateaux[b]) if (i, y) in self.coups_prep and self.coups_prep[(i, y)][b]), # les positions en dessous de (x, y)
                    ((x, j) for j in range(y+1, y+bateaux[b]) if (x, j) in self.coups_prep and self.coups_prep[(x, j)][b]),
                    ((x, j) for j in range(y-1, y-bateaux[b]-1, -1) if (x, j) in self.coups_prep and self.coups_prep[(x, j)][b])
                ):
                self.coups_prep.move_to_end(c) # on bouge les positions en fin du dict (elle seront donc appelées en premier sur un popitem)
        else: # le coup n'a rien touché
            # les beataux sont contigus
            if (pb := (x+1, y)) in self.coups_joue: 
                for (i, y) in [(i, y) for i in range(x, -1, -1) if (i, y) in self.coups_prep]:
                    self.coups_prep[(i, y)][self.coups_joue[pb]] = 0
            if (ph := (x-1, y)) in self.coups_joue: 
                for (i, y) in [(i, y) for i in range(x, 10) if (i, y) in self.coups_prep]:
                    self.coups_prep[(i, y)][self.coups_joue[ph]] = 0
            if (pd := (x, y+1)) in self.coups_joue: 
                for (x, j) in [(x, j) for j in range(y, -1, -1) if (x, j) in self.coups_prep]:
                    self.coups_prep[(x, j)][self.coups_joue[pd]] = 0                 
            if (pg := (x, y-1)) in self.coups_joue: 
                for (x, j) in [(x, j) for j in range(y, 10) if (x, j) in self.coups_prep]:
                    self.coups_prep[(x, j)][self.coups_joue[pg]] = 0

        # TODO: nettoyer les coups prep en enlevant les coups dont la liste des possibilité est vide

        self.coups_joue[(x, y)] = b
    
        return (x, y)

def genere_mat_proba(taille_bat, pos=None):
    
    if not pos:
        r = np.empty( (10, 10) )
        for i in range(0, 10):
            for j in range(0, 10):
                a = 5-abs(i-4) if (i-4 <= 0) else 10-i
                b = 5-abs(j-4) if (j-4 <= 0) else 10-j
                r[i][j] = min(a+b, 2*taille_bat)

    else:
        r = np.zeros( (10, 10) )
        (x, y) = pos

        for i in range(max(x-taille_bat+1, 0), min(x, 10-taille_bat+2)):
            r[i:i+taille_bat+1, y] = [k+1 for k in r[i:i+taille_bat+1, y]]

        for j in range(max(y-taille_bat+1, 0), min(y, 10-taille_bat+2)):
            r[x, j:j+taille_bat+1] = [l+1 for l in r[x, j:j+taille_bat+1]]

    return r

class JoueurProba(Joueur):

    def __init__(self, bataille):
        
        Joueur.__init__(self, bataille)

        m = dict( map( lambda k : (k, genere_mat_proba(bateaux[k])), bateaux.keys() ) )

        for id_bat, taille_bat in bateaux:
            m += (genere_mat_proba(taille_bat), )

        self.coups_prep = OrderedDict()
        for (x, y) in [ pos for pos in itr.product(range(10), range(10)) ]:
            self.coups_prep[(x, y)] = dict( map( lambda k: (k, m[k][x][y]), bateaux.keys() ) )

        self.coups_joue = OrderedDict()
        
            
        def joue():

            self.coups_prep = OrderedDict( sorted( self.coups_prep.items(), key=lambda x: np.sum(x[1]) ) ) # on réorganise l'ordre du dictionnaire en fonction de la probabilité d'un coup de toucher un bateau

            (x, y) = self.bataille.liste_coups.popitem()
            
            b = self.bataille.joue( (x, y) ) # si le coup touche
            if b:
                m = genere_mat_proba(bateaux[b], (x, y))

                for (i,j), p in self.coups_prep:
                    p[b] = m[i][j]
            
            else:
                m = genere_mat_proba(bateaux[b], (x, y))

                for (i,j), p in self.coups_prep:
                    p[b] -= m[i][j]

            for (i,j), p in self.coups_prep:
                for bb in bateaux.keys():
                    if bb != b:
                        p[bb] = 0

            return (x, y)