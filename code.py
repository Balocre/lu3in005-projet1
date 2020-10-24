import random
import numpy as np
import matplotlib.pyplot as plt
import itertools as itr
import warnings
from typing import Optional
import math
from collections import OrderedDict

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
        self.coups_prep = OrderedDict([(i, dict.fromkeys(bateaux.keys, 1)) for i in self.liste_coups])
        self.coups_joue = OrderedDict()        

    # TODO: 
    # traiter l'épuisement des cases
    def joue(self):

        (x, y) = self.bataille.liste_coups.popitem()
        if b := self.bataille.joue( (x, y) ): # si le coup touche

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
                    ((i, y) for i in range(x-1, x-bateaux[b], -1) if (i, y) in self.coups_prep and self.coups_prep[(i, y)][b]),
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
    
        return (x, y)

def genere_mat_proba(taille_bat, pos=None):
    
    if not pos:
        r = np.empty( (5, 1) )
        c = taille_bat
        for k in range(5):
            r[k] = min(c, abs(k)) + 1
            print("rk = {}".format(r[k]))
    
        r = np.tile(r, (1, 5))
        r = r + np.transpose(r)
        r = np.concatenate( (r, np.flip(r, 1)), 1 )
        r = np.concatenate( (r, np.flip(r)))

    else:
        r = np.zeros( (10, 10) )
        (x, y) = pos
        for i in range(x-math.ceil(taille_bat/2), x+math.ceil(taille_bat/2)):
            r[i][y] = 1
        for j in range(y-math.ceil(taille_bat/2), y+math.ceil(taille_bat/2)):
            r[x][j] = 1

    r /= np.sum(r) # on divise chaque élément par le poids toal des élements

    return r

# class JoueurProba(Joueur):

#     def __init__(self, bataille):
#         Joueur.__init__(self, bataille)

#         self.tab_mat_p = dict()

#         for id_bat, taille_bat in bateaux:
#             self.tab_mat_p[id_bat] = genere_mat_proba(taille_bat)
            

#     def joue(self):

#         mat_p_tot = np.sum([m for m in self.tab_mat_p])

#         pos = np.unravel_index(np.argmax(mat_p_tot, axis=None), mat_p_tot.shape) # on obtient la position du premier élément de proba max
        
#         id_bat_touche = self.bataille.joue(pos)

#         if id_bat_touche and id_bat_touche not in self.bataille.liste_touche: # si le coup a touché mais le bateau n'était pas encore touché
#             self.tab_mat_p[id_bat_touche] = genere_mat_proba(bateaux[id_bat_touche], pos)
#             for i in self.tab_mat_p and i != id_bat_touche:
#                 self.tab_mat_p[i][pos] = 0 # on passe à 0 la proba de toucher les bateaux en posisition pos
#                 self.tab_mat_p[i] /= np.sum(self.tab_mat_p[i]) # on recalcul les probas des autres cases de contenir le bateau i

#         elif id_bat_touche and id_bat_touche in self.bataille.liste_touche:
#             (x, y) = pos
#             for cx, cy in self.bataille.liste_coups and self.bataille.grille_decouvert[cx][cy] == id_bat_touche:
#                 if (cx, y) == (x-1, y):

#             self.tab_mat_p[id_bat_touche][pos] = 0
