import random
import numpy as np
import matplotlib.pyplot as plt
import itertools as itr
import warnings
from typing import Optional
from typing import Tuple
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

def peut_placer(bateaux, grille, id_bat, pos, direction):
    """Teste s'il est possible de placer un bateau sur la grille de jeu.

    Args:
        grille (int[][]): Matrice représentant la grille de jeu.
        bateau (int): Id du bateau.
        position (int*int): Position de l'origine du bateau dans la grille de jeu.
        direction (String): Direction en fonctions des axes x (vertical) et y (horisontal) \"+x\" pour horizontal-droite, \"+y\" pour vertical-bas.

    Returns:
        bool: True si le bateau peut être placé, False sinon.
    """

    directions = frozenset(["+x", "+y"])
    if direction not in directions: raise ValueError("{} n'est pas une direction valide".format(direction))

    x, y = pos
    taille_bat = bateaux[id_bat]

    if (x < 0) or (y < 0) or (x + taille_bat >= N) or (y + taille_bat >= N): return False # on vérifie que les coordonées sont dans la grille

    if (direction == "+y"): # horizontale vers la droite
       if not np.all(grille[x, y:y+taille_bat]): return True # on vérifie que les cases de la grille sont libres

    elif (direction == "+x"): # verticale vers le bas
       if not np.count_nonzero(grille[x:x+taille_bat, y]): return True
    
    return False

def place(bateaux, grille, id_bat, pos, direction) -> Optional[Tuple[Tuple[int, int], ...]]:
    """Place un bateau sur la grille de jeu si c'est possible.

    Args:
        grille (int[][]): Matrice représentant la grille de jeu.
        bateau (int): Id du bateau.
        position (int*int): Position dans la matrice. 
        direction (String): Direction en fonctions des axes x (vertical) et y (horisontal) \"+x\" pour horizontal-droite, \"+y\" pour vertical-bas.

    Returns:
        Optional[tuple(tuple())]: Tuple de coordonées si le bateau à été placé None sinon
    """
    x, y = pos
    taille_bat = bateaux[id_bat]

    if not peut_placer(bateaux, grille, id_bat, pos, direction): 
        return None
    
    else:
        if (direction == "+y"): 
            grille[x, y:y+taille_bat] = id_bat
            return tuple( (x, j) for j in range(y, y+taille_bat) )

        elif (direction == "+x"):
            grille[x:x+taille_bat, y] = id_bat
            return tuple( (i, y) for i in range(x, x+taille_bat) )


def place_alea(bateaux, grille, bateau):
    """Place un bateau à une position aléatoire de la grille de jeu

    Args:
        grille (int[][]): Matrice représentant la grille de jeu.
        bateau (int): Id du bateau.

    Returns:
        tuple(tuple()): Tuple de coordonées
    """

    while r := not place(bateaux, 
        grille, 
        bateau, 
        (random.randint(0, 9), random.randint(0, 9)), 
        random.sample( frozenset(["+x", "+y"]), 1)[0]
        ):
        continue

    return r


def affiche(grille):
    """Affiche l'état de la grille de jeu.
    
    Args:
        grille (int[][]): Matrice représentant la grille de jeu.
    """
    plt.matshow(grille)
    plt.waitforbuttonpress()
    plt.close()

def eq(grille_a, grille_b):
    """Compare 2 grilles pour l'égalité.
    
    Args:
        grille_a (int[][]): Matrice représant la première grille de jeu.
        grille_b (int[][]): Matrice représant la deuxièmé grille de jeu.

    Returns:
        bool: True si les grilles sont égales, False sinon.
    """
    row_a = len(grille_a)
    col_a = len(grille_a[0])

    row_b = len(grille_b)
    col_b = len(grille_b[0])

    if( (row_a != row_b) or (col_a != col_b) ): # si les matrices ne sont pas de tailel égale
        warnings.warn("Les matrices entrées ne sont pas de la même taille")

    if np.array_equal(grille_a, grille_b):
        return True

    return False
    
def genere_grille(bateaux):
    """Génère une grille de jeu aléatoire.

    Returns:
        int[][]: Une matrice représantant une grille de jeu.

    """
    grille = np.zeros( (10, 10) )
    for b in bateaux.keys():
        place_alea(bateaux, grille, b)
    return grille

# Partie 2

def nb_pos(bateaux, grille, bateau):
    """Compte le nombre de facons de placer un bateau dans la grille.

    Args:
        grille (int[][]): Matrice représentant la grille de jeu.
        bateau (int): id du bateau.

    Returns:
        int: Le nombre de positions dans lesquelles on peut placer le bateau.
    """
    cpt = 0
    for i in range(N):
        for j in range(N):
            if (peut_placer(bateaux, grille, bateau,(i,j),"+x")):
                cpt+=1
            if (peut_placer(bateaux, grille, bateau,(i,j),"+y")):
                cpt+=1
    return cpt

def nb_pos_list(grille, L):
    """Euh
    """
    if not L : return 0
    if len(L)==1 : return nb_pos(bateaux, grille,L[0])
    else :
        cpt = 0
        for i in range(N):
            for j in range(N):
                g1 = np.copy(grille)
                if place(bateaux, g1, L[0], (i,j), "+x"): cpt += nb_pos_list(g1, L[1:])
                g2 = np.copy(grille)
                if place(bateaux, g2, L[0], (i,j), "+y"): cpt += nb_pos_list(g2, L[1:])
        return cpt

def comp_alea_grille(bateaux, grille):
    """Compare la grille en entrée à des grilles générées aléatoirement jusqu'a trouver une grille de jeu égale.

    Args:
        grille (int[][]): Matrice représentant la grille de jeu.

    Returns:
        int: Le nombre de grilles générées avant de trouver une grille de jeu égale à l'entrée.
    """
    i = 0
    while True:
        i+=1
        if eq(grille, genere_grille(bateaux)):
            break
    return i

def approx_total_grilles(bateaux, n):
    """Calcul la moyenne sur n itérations du nombre de grilles générées par comp_alea_grille.

    Args:
        n (int): Nombre d'itérations de comp_alea_grille à éffectuer.
    
    Returns:
        (int): La moyenne du nombre d'itérations éfféctuées.
    """
    r = np.array([])
    g = genere_grille(bateaux)
    for i in range(n):
        np.append(r, comp_alea_grille(bateaux, g))

    return np.average(r)


# Partie 3

class Bataille:
    """Représente une partie de bataille navale 

    Attributes:
        grille (int[][]): Matrice représentant la grille de jeu.
        grille_decouverte (int[][]): Matrice représantant les positions découvertes par le joueur
    """

    def __init__(self, bateaux, grille=None):
        if grille is not None:
            self.grille = grille 
        else:
            self.grille = genere_grille(bateaux)

        # XXX: peut-etre passer en np.empty? si pas de pb lors de la comparaison
        self.grille_decouverte = np.zeros( (10, 10) )

        self.bateaux = bateaux


    def joue(self, pos) -> Optional[int]:
        """Joue un coup à la position pos

        Args:
            pos ((int, int)): La position à laquelle jouer le coup

        Returns:
            Optional[int]: L'id du bateau à la position jouée si il y'a un bateau, None sinon
        """

        (x, y) = pos

        if (x < 0) or (y < 0) or (x > 9) or (y > 9):
            raise ValueError("la position spécifiée n'est pas valide")

        self.grille_decouverte[pos] = self.grille[pos] # on met à jour la carte de découverte

        if self.grille[pos]: # si il y a un bateau ou le joueur vise
            return self.grille[pos] # la fonction renvoie l'id du bateau touché

        return None # la fonction indique que rien n'a été touché

    def victoire(self):
        """Vérifie si la partie est finie.

        Cette fonction compare la grille de jeu et la grille de découverte et si grille_decouverte == grille
        celà signifie que toutes les positions contenant des bateaux ont été jouées et par conséquent que
        la partie est finie.

        Returns:
            bool: True si la partie est finie, False sinon.
        """
        if eq(self.grille, self.grille_decouverte):
            return True
        return False

    def reset(self):
        pass
    
class Joueur:
    """Représente un joueur de bataille navale

    Note:
        Cette classe ne sert que de super classe pour les classes en héritant et ne doit pas être instanciée.
        Utiliser JoueurAlea, JoueurHeur ou JoueurProba.

    Args:
        bataille (Bataille): La bataille jouée par le joueur.

    Attributes:
        bataille (Bataille): La bataille jouée par le joueur.
    """

    def __init__(self, bataille):
        self.bataille = bataille

        self.coups_prep = None

    def joue(self):
        """
        Note:
            Cette méthode ne sert que de placeholder.
        """
        pass

class JoueurAlea(Joueur):
    """Représente un joueur ayant un comportement aléatoire.

    Args:
        bataille (Bataille): La bataille jouée par le joueur.

    Attributes:
        bataille (Bataille): La bataille jouée par le joueur.
        coup_prep (list((int, int))): Liste des coups préparés par le joueur.
            La liste de coup est mélangée après son instanciation.
    """

    def __init__(self, bataille):
        Joueur.__init__(self, bataille)
        
        # génère une liste de position aléatoires dans la grille
        self.coups_prep = list(itr.product(range(10), range(10))) 
        random.shuffle(self.coups_prep)

    def joue(self):
        """Joue un coup de la bataille de manière aléatoire.
        
        Pop un élément de la liste de coup et le joue sur la bataille.

        Returns:
            (int, int): La position du coup joué
        """

        if len(self.coups_prep) == 0:
            warnings.warn("Le joueur ne peux plus jouer, tout ses coups sont épuisés")
            return None

        pos = self.coups_prep.pop() # on pop la position jouée de la liste por ne pas répéter 2 fois un coup inutilement
        self.bataille.joue(pos)

        return pos
    
class JoueurHeur(JoueurAlea): # hérite de joueur aléa, car le comportement par défaut est aléatoire
    """Représente un joueur séléctionnant ses coups à l'aide d'une heuristique.

    Args:
        bataille (Bataille): La bataille jouée par le joueur.

    Attributes:
        coup_prep (OrderedDict of (int, int): dict of int: int): Dictionnaire représantant la suite de coups qui seront joués par le joueur dans l'ordre.
            Les clés du dictionnaire sont les couples représentant la position du coup et les valeurs sont des des dictionnaires dont les clés correspondent 
            aux clés de la liste de bateau auxquelles sont associées 1 si le joeur s'attend à trouver le bateau correspondant à la position et 0 sinon
            Le dictionnaire est initialisé à partir de coup_prep de la superclasse JoueurAlea, coup prep représente donc une suite de coups aléatoires
            après initialisation.
        
        coup_joue (OrderedDict of (int, int): Optional[int]): Dictionnaire représantant les coups joués par le joueur   
    """

    def __init__(self, bataille):
        JoueurAlea.__init__(self, bataille)

        # XXX: utiliser un tuple comme valeur serait certainement plus rapide, dans ce cas corriger les index
        self.coups_prep = OrderedDict([(i, dict.fromkeys(self.bataille.bateaux.keys(), 1)) for i in self.coups_prep]) # ce dictionnaire contient la liste des coups préparés par le joueur, en utilisant pour clé le couple (x, y) représentant la position du coup et ayant pour valeur un dict ayant pour clé les id des bateaux et valeur 1 si on peut trouver le bateau correspondant à la position 0 sinon 
        self.coups_joue = OrderedDict() # ce dict contient la liste des coups joués, en utilisant pour clé le couple (x, y) représentant la position du coup et ayant pour valeur l'id du bateau trouvé à la position ou None

    # TODO: 
    # traiter l'épuisement des cases
    def joue(self):
        """Joue un coup de la bataille en utilisant une heuristique.

        L'heuristique est la suivante:
        Dans le cas par défaut joue un coup aléatoire de la bataille.
        Si le coup touche: 
            * élimine les positions rendues impossibles par la découverte du bateau touché à la position jouée - essentiellement les positions 
              qui seraient coupées par une case déjà jouée ne contenant pas le bateau découvert.
            * éxplore les cases pouvant contenir le bateau touché en croix autours de la position jouée avec pour distance max du centre de la 
              croix la taille du bateau.
        Sinon :
            * vérifie si la cases autours de de la position jouée ont déjà été jouées et si un bateau y a été découvert, si oui élimine la possibilité de trouver ce
              bateau dans les cases noon jouées de la direction opposée.

        Returns:
            (int, int): La position du coup joué.
        """

        if not self.coups_prep:
            warnings.warn("Le joueur ne peux plus jouer, tout ses coups sont épuisés")
            return None

        x, y = self.coups_prep.popitem()[0]
        b = self.bataille.joue( (x, y) ) # si le coup touche
        if b:
            # on retire la possibilité de trouver b aux positions potentielles "plus loin" qu'une position ayant déjà étée jouée avec un autre bateau que b ait été découvert ou dont on à éliminé la possibilité de contenir b
            for (i, y) in [(i, y) for i in range(x-1, x-self.bataille.bateaux[b], -1) if ( ( (i, y) in self.coups_prep and not self.coups_prep[(i, y)][b] ) or ( (i, y) in self.coups_joue and self.coups_joue[(i, y)] != b ))]: # pour les positions n'ayant pas été jouées et ne pouvant pas contenir b et les position ayant été jouées et contenant un autre bateau que b
                for (k, y) in [(k, y) for k in range(0, i) if (k, y) in self.coups_prep]: # pour les positions au-dessus d'une position matchée par l'expression ci-dessus
                    if (i , y) in self.coups_prep:
                        self.coups_prep[(i, y)][b] = 0 # on passe la valeur associée à la clé b à 0
            for (i, y) in [(i, y) for i in range(x+1, x+self.bataille.bateaux[b]) if ( ( (i, y) in self.coups_prep and not self.coups_prep[(i, y)][b] ) or ( (i, y) in self.coups_joue and self.coups_joue[(i, y)] != b ))]:
                for (k, y) in [(k, y) for k in range(10, i, -1) if (k, y) in self.coups_prep]:
                    if (i , y) in self.coups_prep:
                        self.coups_prep[(i, y)][b] = 0
            for (x, j) in [(x, j) for j in range(y+1, y+self.bataille.bateaux[b]) if ( ( (x, j) in self.coups_prep and not self.coups_prep[(x, j)][b] ) or ( (x, j) in self.coups_joue and self.coups_joue[(x, j)] != b ))]:
                for (x, l) in [(x, l) for l in range(10, j, -1) if (x, l) in self.coups_prep]:
                    if (x , l) in self.coups_prep:
                        self.coups_prep[(x, l)][b] = 0
            for (x, j) in [(x, j) for j in range(y-1, y-self.bataille.bateaux[b], -1) if ( ( (x, j) in self.coups_prep and not self.coups_prep[(x, j)][b] ) or ( (x, j) in self.coups_joue and self.coups_joue[(x, j)] != b ))]:
                for (x, l) in [(x, l) for l in range(0, j) if (x, l) in self.coups_prep]:
                    if (x , l) in self.coups_prep:
                        self.coups_prep[(x, l)][b] = 0
            

            # on augemnte la priorité des coups sur les positions pouvant potentiellement contenir le bateau b i.e. une croix autours de la position du b touché
            for c in itr.chain( # on itère sur des générateurs décrivant ces positions
                    # XXX: peu se faire avec une compréhension de liste
                    ((i, y) for i in range(x-1, x-self.bataille.bateaux[b]-1, -1) if (i, y) in self.coups_prep and self.coups_prep[(i, y)][b]),
                    ((i, y) for i in range(x+1, x+self.bataille.bateaux[b]) if (i, y) in self.coups_prep and self.coups_prep[(i, y)][b]), # les positions en dessous de (x, y)
                    ((x, j) for j in range(y+1, y+self.bataille.bateaux[b]) if (x, j) in self.coups_prep and self.coups_prep[(x, j)][b]),
                    ((x, j) for j in range(y-1, y-self.bataille.bateaux[b]-1, -1) if (x, j) in self.coups_prep and self.coups_prep[(x, j)][b])
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
    """Génère une matrice de probabilité pour le bateau de taille donnée.

    Cette fonction peut générer deux types de matrices de probabilité :
        * Dans le cas où la position de l'origine du bateau n'est pas donnée, la matrice de proba générée correspond à la superposition de tous les bateaux possibles
          sur la grille.
        * Dans l'autre cas la matrice de proba correspond à la superposition des bateaux ayant une pièce placée sur l'origine

    Args:
        taille_bat (int): La taille du bateau pour lequel générer la matrice de proba
        pos ((int, int), optional): La position de l'origine du bateau, None par défaut

    Returns:
        int[][]: La matrice de probabilité associée au bateau de taille passée en entrée
    """
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
    """Représente un joueur qui choisi ses coups en fcontion des probabilités de toucher un bateau

    Args:
        bataille (Bataille): La bataille jouée par le joueur.

    Attributes:
        bataille (Bataille): La bataille jouée par le joueur.
        coup_prep (OrderedDict of (int, int): dict of int: int): Dictionnaire représantant la suite de coups qui seront joués par le joueur dans l'ordre.
            la suite de coup est ordonée en fonction des probabilités associées au coup avant de jouer un coup sur la bataille
        coup_joue (OrderedDict of (int, int): Optional[int]): Dictionnaire représantant les coups joués par le joueur 
    """

    def __init__(self, bataille):
        
        Joueur.__init__(self, bataille)

        m = dict( map( lambda k : (k, genere_mat_proba(self.bataille.bateaux[k])), self.bataille.bateaux.keys() ) )

        # for id_bat, taille_bat in self.bataille.bateaux.items():
        #     m += (genere_mat_proba(taille_bat), )

        self.coups_prep = OrderedDict()
        for (x, y) in [ pos for pos in itr.product(range(10), range(10)) ]:
            self.coups_prep[(x, y)] = dict( map( lambda k: (k, m[k][x][y]), self.bataille.bateaux.keys() ) )

        self.coups_joue = OrderedDict()
        
            
    def joue(self):
        """Joue un coup de la bataille parmis les coups ayant la plus grande proba de toucher un bateau

        Returns:
            (int, int): La position du coup joué.
        """

        if not self.coups_prep:
            warnings.warn("Le joueur ne peux plus jouer, tout ses coups sont épuisés")
            return None

        self.coups_prep = OrderedDict( sorted( self.coups_prep.items(), key=lambda x: sum(x[1].values() ) ) ) # on réorganise l'ordre du dictionnaire en fonction de la probabilité d'un coup de toucher un bateau

        x, y = self.coups_prep.popitem()[0]

        b = self.bataille.joue( (x, y) ) # si le coup touche
        if b:
            m = genere_mat_proba(self.bataille.bateaux[b], (x, y))

            for (i,j), p in self.coups_prep.items():
                p[b] = m[i][j]
        
        else:
            for b in self.bataille.bateaux.keys():
                m = genere_mat_proba(self.bataille.bateaux[b], (x, y))

                for (i,j), p in self.coups_prep.items():
                    p[b] -= m[i][j]

        for (i,j), p in self.coups_prep.items():
            for bb in self.bataille.bateaux.keys():
                if bb != b:
                    p[bb] = 0

        return (x, y)
