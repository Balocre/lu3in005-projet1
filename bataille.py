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

#Repr├⌐sentation du plateau vide en tant que matrice 10x10
plateau = np.zeros( (10,10) )

# Partie 1

def peut_placer(bateaux, grille, id_bat, pos, direction):
    """Teste s'il est possible de placer un bateau sur la grille de jeu.

    Args:
        grille (int[][]): Matrice repr├⌐sentant la grille de jeu.
        bateau (int): Id du bateau.
        position (int*int): Position de l'origine du bateau dans la grille de jeu.
        direction (String): Direction en fonctions des axes x (vertical) et y (horisontal) \"+x\" pour horizontal-droite, \"+y\" pour vertical-bas.

    Returns:
        bool: True si le bateau peut ├¬tre plac├⌐, False sinon.
    """

    directions = frozenset(["+x", "+y"])
    if direction not in directions: raise ValueError("{} n'est pas une direction valide".format(direction))

    x, y = pos
    taille_bat = bateaux[id_bat]

    if (x < 0) or (y < 0) or (x + taille_bat >= N) or (y + taille_bat >= N): return False # on v├⌐rifie que les coordon├⌐es sont dans la grille

    if (direction == "+y"): # horizontale vers la droite
       if not np.all(grille[x, y:y+taille_bat]): return True # on v├⌐rifie que les cases de la grille sont libres

    elif (direction == "+x"): # verticale vers le bas
       if not np.count_nonzero(grille[x:x+taille_bat, y]): return True
    
    return False

def place(bateaux, grille, id_bat, pos, direction) -> Optional[Tuple[Tuple[int, int], ...]]:
    """Place un bateau sur la grille de jeu si c'est possible.

    Args:
        grille (int[][]): Matrice repr├⌐sentant la grille de jeu.
        bateau (int): Id du bateau.
        position (int*int): Position dans la matrice. 
        direction (String): Direction en fonctions des axes x (vertical) et y (horisontal) \"+x\" pour horizontal-droite, \"+y\" pour vertical-bas.

    Returns:
        Optional[tuple(tuple())]: Tuple de coordon├⌐es si le bateau ├á ├⌐t├⌐ plac├⌐ None sinon
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
    """Place un bateau ├á une position al├⌐atoire de la grille de jeu

    Args:
        grille (int[][]): Matrice repr├⌐sentant la grille de jeu.
        bateau (int): Id du bateau.

    Returns:
        tuple(tuple()): Tuple de coordon├⌐es
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
    """Affiche l'├⌐tat de la grille de jeu.
    
    Args:
        grille (int[][]): Matrice repr├⌐sentant la grille de jeu.
    """
    plt.matshow(grille)
    plt.waitforbuttonpress()
    plt.close()

def eq(grille_a, grille_b):
    """Compare 2 grilles pour l'├⌐galit├⌐.
    
    Args:
        grille_a (int[][]): Matrice repr├⌐sant la premi├¿re grille de jeu.
        grille_b (int[][]): Matrice repr├⌐sant la deuxi├¿m├⌐ grille de jeu.

    Returns:
        bool: True si les grilles sont ├⌐gales, False sinon.
    """
    row_a = len(grille_a)
    col_a = len(grille_a[0])

    row_b = len(grille_b)
    col_b = len(grille_b[0])

    if( (row_a != row_b) or (col_a != col_b) ): # si les matrices ne sont pas de tailel ├⌐gale
        warnings.warn("Les matrices entr├⌐es ne sont pas de la m├¬me taille")

    if np.array_equal(grille_a, grille_b):
        return True

    return False
    
def genere_grille(bateaux):
    """G├⌐n├¿re une grille de jeu al├⌐atoire.

    Returns:
        int[][]: Une matrice repr├⌐santant une grille de jeu.

    """
    grille = np.zeros( (10, 10) )
    for b in bateaux.keys():
        place_alea(bateaux, grille, b)
    return grille

# Partie 2

def nb_pos(bateaux, grille, bateau):
    """Compte le nombre de facons de placer un bateau dans la grille.

    Args:
        grille (int[][]): Matrice repr├⌐sentant la grille de jeu.
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
    """Compare la grille en entr├⌐e ├á des grilles g├⌐n├⌐r├⌐es al├⌐atoirement jusqu'a trouver une grille de jeu ├⌐gale.

    Args:
        grille (int[][]): Matrice repr├⌐sentant la grille de jeu.

    Returns:
        int: Le nombre de grilles g├⌐n├⌐r├⌐es avant de trouver une grille de jeu ├⌐gale ├á l'entr├⌐e.
    """
    i = 0
    while True:
        i+=1
        if eq(grille, genere_grille(bateaux)):
            break
    return i

def approx_total_grilles(bateaux, n):
    """Calcul la moyenne sur n it├⌐rations du nombre de grilles g├⌐n├⌐r├⌐es par comp_alea_grille.

    Args:
        n (int): Nombre d'it├⌐rations de comp_alea_grille ├á ├⌐ffectuer.
    
    Returns:
        (int): La moyenne du nombre d'it├⌐rations ├⌐ff├⌐ctu├⌐es.
    """
    r = np.array([])
    g = genere_grille(bateaux)
    for i in range(n):
        np.append(r, comp_alea_grille(bateaux, g))

    return np.average(r)

def approx_total_grilles_2(bateaux, n):
    """
    Calcule la moyenne sur n itérations du nombre de combinaisons possibles.

    -Calcule, pour chaque bateau, le nombre nb de façons de le poser dans une grille initialement vide
    -Le place aléatoirement dans celle-ci. 
    -La multiplication des nb donne le nombre de combinaisons possibles pour une seule grille. 
    -Repète cette opération n fois
    -Retourne la moyenne
    Args:
        n (int): Nombre d'itérations de comp_alea_grille à éffectuer.
    
    Returns:
        int: La moyenne du nombre d'itérations éffectuées.
    """
    cpt = 0
    for i in range(n):
        g = np.zeros((N, N))
        nb = 1
        for b in bateaux :
            nb *= nb_pos(bateaux, g, b)
            place_alea(bateaux,g,b)
        cpt += nb
    return cpt/n


def approx_total_grilles_3(bateaux,n):
    """
    Calcule la moyenne sur n itérations du nombre de combinaisons possibles.

    -On génère aléatoirement n grilles avec les 3 premiers bateaux
    -On calcule exactement n fois le nombre de combinaisons des 2 bateaux restants sur ces grilles pour trouver la valeur moyenne.
    -Retourne la multiplication de cette moyenne par le nombre de combinaisons des 3 premiers bateaux sur une grille vide.
    Args:
        n (int): Nombre d'itérations de comp_alea_grille à éffectuer.
    
    Returns:
        int: La moyenne du nombre d'itérations éffectuées.
    """
    L = []
    for k in bateaux:
        L.append(k)
    cpt=0
    for i in range (n):
        g = np.zeros((10,10))
        for j in range(3):
            place_alea(bateaux,g,L[j])
        cpt += nb_pos_list(g, L[3:])
    return cpt/n * nb_pos_list(np.zeros((N,N)), L[:3])


# Partie 3

class Bataille:
    """Repr├⌐sente une partie de bataille navale 

    Attributes:
        grille (int[][]): Matrice repr├⌐sentant la grille de jeu.
        grille_decouverte (int[][]): Matrice repr├⌐santant les positions d├⌐couvertes par le joueur
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
        """Joue un coup ├á la position pos

        Args:
            pos ((int, int)): La position ├á laquelle jouer le coup

        Returns:
            Optional[int]: L'id du bateau ├á la position jou├⌐e si il y'a un bateau, None sinon
        """

        (x, y) = pos

        if (x < 0) or (y < 0) or (x > 9) or (y > 9):
            raise ValueError("la position sp├⌐cifi├⌐e n'est pas valide")

        self.grille_decouverte[pos] = self.grille[pos] # on met ├á jour la carte de d├⌐couverte

        if self.grille[pos]: # si il y a un bateau ou le joueur vise
            return self.grille[pos] # la fonction renvoie l'id du bateau touch├⌐

        return None # la fonction indique que rien n'a ├⌐t├⌐ touch├⌐

    def victoire(self):
        """V├⌐rifie si la partie est finie.

        Cette fonction compare la grille de jeu et la grille de d├⌐couverte et si grille_decouverte == grille
        cel├á signifie que toutes les positions contenant des bateaux ont ├⌐t├⌐ jou├⌐es et par cons├⌐quent que
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
    """Repr├⌐sente un joueur de bataille navale

    Note:
        Cette classe ne sert que de super classe pour les classes en h├⌐ritant et ne doit pas ├¬tre instanci├⌐e.
        Utiliser JoueurAlea, JoueurHeur ou JoueurProba.

    Args:
        bataille (Bataille): La bataille jou├⌐e par le joueur.

    Attributes:
        bataille (Bataille): La bataille jou├⌐e par le joueur.
    """

    def __init__(self, bataille):
        self.bataille = bataille

        self.coups_prep = None

    def joue(self):
        """
        Note:
            Cette m├⌐thode ne sert que de placeholder.
        """
        pass

class JoueurAlea(Joueur):
    """Repr├⌐sente un joueur ayant un comportement al├⌐atoire.

    Args:
        bataille (Bataille): La bataille jou├⌐e par le joueur.

    Attributes:
        bataille (Bataille): La bataille jou├⌐e par le joueur.
        coup_prep (list((int, int))): Liste des coups pr├⌐par├⌐s par le joueur.
            La liste de coup est m├⌐lang├⌐e apr├¿s son instanciation.
    """

    def __init__(self, bataille):
        Joueur.__init__(self, bataille)
        
        # g├⌐n├¿re une liste de position al├⌐atoires dans la grille
        self.coups_prep = list(itr.product(range(10), range(10))) 
        random.shuffle(self.coups_prep)

    def joue(self):
        """Joue un coup de la bataille de mani├¿re al├⌐atoire.
        
        Pop un ├⌐l├⌐ment de la liste de coup et le joue sur la bataille.

        Returns:
            (int, int): La position du coup jou├⌐
        """

        if len(self.coups_prep) == 0:
            warnings.warn("Le joueur ne peux plus jouer, tout ses coups sont ├⌐puis├⌐s")
            return None

        pos = self.coups_prep.pop() # on pop la position jou├⌐e de la liste por ne pas r├⌐p├⌐ter 2 fois un coup inutilement
        self.bataille.joue(pos)

        return pos
    
class JoueurHeur(JoueurAlea): # h├⌐rite de joueur al├⌐a, car le comportement par d├⌐faut est al├⌐atoire
    """Repr├⌐sente un joueur s├⌐l├⌐ctionnant ses coups ├á l'aide d'une heuristique.

    Args:
        bataille (Bataille): La bataille jou├⌐e par le joueur.

    Attributes:
        coup_prep (OrderedDict of (int, int): dict of int: int): Dictionnaire repr├⌐santant la suite de coups qui seront jou├⌐s par le joueur dans l'ordre.
            Les cl├⌐s du dictionnaire sont les couples repr├⌐sentant la position du coup et les valeurs sont des des dictionnaires dont les cl├⌐s correspondent 
            aux cl├⌐s de la liste de bateau auxquelles sont associ├⌐es 1 si le joeur s'attend ├á trouver le bateau correspondant ├á la position et 0 sinon
            Le dictionnaire est initialis├⌐ ├á partir de coup_prep de la superclasse JoueurAlea, coup prep repr├⌐sente donc une suite de coups al├⌐atoires
            apr├¿s initialisation.
        
        coup_joue (OrderedDict of (int, int): Optional[int]): Dictionnaire repr├⌐santant les coups jou├⌐s par le joueur   
    """

    def __init__(self, bataille):
        JoueurAlea.__init__(self, bataille)

        # XXX: utiliser un tuple comme valeur serait certainement plus rapide, dans ce cas corriger les index
        self.coups_prep = OrderedDict([(i, dict.fromkeys(self.bataille.bateaux.keys(), 1)) for i in self.coups_prep]) # ce dictionnaire contient la liste des coups pr├⌐par├⌐s par le joueur, en utilisant pour cl├⌐ le couple (x, y) repr├⌐sentant la position du coup et ayant pour valeur un dict ayant pour cl├⌐ les id des bateaux et valeur 1 si on peut trouver le bateau correspondant ├á la position 0 sinon 
        self.coups_joue = OrderedDict() # ce dict contient la liste des coups jou├⌐s, en utilisant pour cl├⌐ le couple (x, y) repr├⌐sentant la position du coup et ayant pour valeur l'id du bateau trouv├⌐ ├á la position ou None

    # TODO: 
    # traiter l'├⌐puisement des cases
    def joue(self):
        """Joue un coup de la bataille en utilisant une heuristique.

        L'heuristique est la suivante:
        Dans le cas par d├⌐faut joue un coup al├⌐atoire de la bataille.
        Si le coup touche: 
            * ├⌐limine les positions rendues impossibles par la d├⌐couverte du bateau touch├⌐ ├á la position jou├⌐e - essentiellement les positions 
              qui seraient coup├⌐es par une case d├⌐j├á jou├⌐e ne contenant pas le bateau d├⌐couvert.
            * ├⌐xplore les cases pouvant contenir le bateau touch├⌐ en croix autours de la position jou├⌐e avec pour distance max du centre de la 
              croix la taille du bateau.
        Sinon :
            * v├⌐rifie si la cases autours de de la position jou├⌐e ont d├⌐j├á ├⌐t├⌐ jou├⌐es et si un bateau y a ├⌐t├⌐ d├⌐couvert, si oui ├⌐limine la possibilit├⌐ de trouver ce
              bateau dans les cases noon jou├⌐es de la direction oppos├⌐e.

        Returns:
            (int, int): La position du coup jou├⌐.
        """

        if not self.coups_prep:
            warnings.warn("Le joueur ne peux plus jouer, tout ses coups sont ├⌐puis├⌐s")
            return None

        x, y = self.coups_prep.popitem()[0]
        b = self.bataille.joue( (x, y) ) # si le coup touche
        if b:
            # on retire la possibilit├⌐ de trouver b aux positions potentielles "plus loin" qu'une position ayant d├⌐j├á ├⌐t├⌐e jou├⌐e avec un autre bateau que b ait ├⌐t├⌐ d├⌐couvert ou dont on ├á ├⌐limin├⌐ la possibilit├⌐ de contenir b
            for (i, y) in [(i, y) for i in range(x-1, x-self.bataille.bateaux[b], -1) if ( ( (i, y) in self.coups_prep and not self.coups_prep[(i, y)][b] ) or ( (i, y) in self.coups_joue and self.coups_joue[(i, y)] != b ))]: # pour les positions n'ayant pas ├⌐t├⌐ jou├⌐es et ne pouvant pas contenir b et les position ayant ├⌐t├⌐ jou├⌐es et contenant un autre bateau que b
                for (k, y) in [(k, y) for k in range(0, i) if (k, y) in self.coups_prep]: # pour les positions au-dessus d'une position match├⌐e par l'expression ci-dessus
                    if (i , y) in self.coups_prep:
                        self.coups_prep[(i, y)][b] = 0 # on passe la valeur associ├⌐e ├á la cl├⌐ b ├á 0
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
            

            # on augemnte la priorit├⌐ des coups sur les positions pouvant potentiellement contenir le bateau b i.e. une croix autours de la position du b touch├⌐
            for c in itr.chain( # on it├¿re sur des g├⌐n├⌐rateurs d├⌐crivant ces positions
                    # XXX: peu se faire avec une compr├⌐hension de liste
                    ((i, y) for i in range(x-1, x-self.bataille.bateaux[b]-1, -1) if (i, y) in self.coups_prep and self.coups_prep[(i, y)][b]),
                    ((i, y) for i in range(x+1, x+self.bataille.bateaux[b]) if (i, y) in self.coups_prep and self.coups_prep[(i, y)][b]), # les positions en dessous de (x, y)
                    ((x, j) for j in range(y+1, y+self.bataille.bateaux[b]) if (x, j) in self.coups_prep and self.coups_prep[(x, j)][b]),
                    ((x, j) for j in range(y-1, y-self.bataille.bateaux[b]-1, -1) if (x, j) in self.coups_prep and self.coups_prep[(x, j)][b])
                ):
                self.coups_prep.move_to_end(c) # on bouge les positions en fin du dict (elle seront donc appel├⌐es en premier sur un popitem)
        else: # le coup n'a rien touch├⌐
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

        # TODO: nettoyer les coups prep en enlevant les coups dont la liste des possibilit├⌐ est vide

        self.coups_joue[(x, y)] = b
    
        return (x, y)

def genere_mat_proba(taille_bat, pos=None):
    """G├⌐n├¿re une matrice de probabilit├⌐ pour le bateau de taille donn├⌐e.

    Cette fonction peut g├⌐n├⌐rer deux types de matrices de probabilit├⌐ :
        * Dans le cas o├╣ la position de l'origine du bateau n'est pas donn├⌐e, la matrice de proba g├⌐n├⌐r├⌐e correspond ├á la superposition de tous les bateaux possibles
          sur la grille.
        * Dans l'autre cas la matrice de proba correspond ├á la superposition des bateaux ayant une pi├¿ce plac├⌐e sur l'origine

    Args:
        taille_bat (int): La taille du bateau pour lequel g├⌐n├⌐rer la matrice de proba
        pos ((int, int), optional): La position de l'origine du bateau, None par d├⌐faut

    Returns:
        int[][]: La matrice de probabilit├⌐ associ├⌐e au bateau de taille pass├⌐e en entr├⌐e
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
    """Repr├⌐sente un joueur qui choisi ses coups en fcontion des probabilit├⌐s de toucher un bateau

    Args:
        bataille (Bataille): La bataille jou├⌐e par le joueur.

    Attributes:
        bataille (Bataille): La bataille jou├⌐e par le joueur.
        coup_prep (OrderedDict of (int, int): dict of int: int): Dictionnaire repr├⌐santant la suite de coups qui seront jou├⌐s par le joueur dans l'ordre.
            la suite de coup est ordon├⌐e en fonction des probabilit├⌐s associ├⌐es au coup avant de jouer un coup sur la bataille
        coup_joue (OrderedDict of (int, int): Optional[int]): Dictionnaire repr├⌐santant les coups jou├⌐s par le joueur 
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
            (int, int): La position du coup jou├⌐.
        """

        if not self.coups_prep:
            warnings.warn("Le joueur ne peux plus jouer, tout ses coups sont ├⌐puis├⌐s")
            return None

        self.coups_prep = OrderedDict( sorted( self.coups_prep.items(), key=lambda x: sum(x[1].values() ) ) ) # on r├⌐organise l'ordre du dictionnaire en fonction de la probabilit├⌐ d'un coup de toucher un bateau

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

class Senseur():
    def __init__(self, n, p,repar):
        """
        Constructeur : initialise les dimensions, la matrice de probabilit├⌐ et la repartition.
        Args :
            n (int) : nombre de lignes
            p (int) : nombre de colonnes
            repar (int) : repartition - 1 pour centree - 2 en bordure - 3 gauche nul - sinon aleatoire
        """
        mat_p = self.genere_mat_proba_senseur(n,p,repar) #matrice de probabilite
        self.place_senseur(n,p) #initialise l'attribut pos

    def place_senseur(self,n,p):
        """
        Initialise l'attribut pos qui correspond au tuple (i,j) repr├⌐sentant la position
        du sous-marin
        Args:
        n (int) : nombre de lignes
        p (int) : nombre de colonnes
        """
        s=0
        k = random.random()
        for i in range(n):
            for j in range(p):
                if (k < s + self.mat_p[i][j]):
                    self.pos=(i,j)
                    return None
                s = s + self.mat_p[i][j]
        print("Erreur place_senseur")
        return None

    def genere_mat_proba_senseur(self,n,p,repar):
        """Retourne une matrice de probabilit├⌐ N*P selon une distribution repar.
        Args : 
            n (int): nombre de lignes
            p (int): nombre de colonnes
            repar (int): repartition choisie. 1 pour centree, 2 pour favoriser la bordure
                    3 pour defavoriser le flanc gauche, sinon pour aleatoire
        """
        self.mat_p = np.empty((n,p), dtype=float)
        c = (n+p)*50
        #repartition aleatoire, repar = 0
        for i in range(n):
            for j in range(p):
                self.mat_p[i][j]=float(random.randint(0,c))
        if (repar==1):
        #repartition centree
            for i in range(int(n/2),int(n/2+1)):
                for j in range(int(p/2),int(p/2+1)):
                    self.mat_p[i][j]=float(random.randint(4*c,6*c))
        
        elif (repar == 2):
            #repartition bords
            for i in [0,n-1]:
                for j in range(p):
                    self.mat_p[i][j]=float(random.randint(3*c,4*c))
            for j in [0,n-1]:
                for i in range(n):
                    self.mat_p[i][j]=float(random.randint(3*c,4*c))
        elif (repar == 3):
        #eviter le flanc gauche
            for i in range(n):
                for j in range(2):
                    if (j<p):
                        self.mat_p[i][j]=0
        d = np.sum(self.mat_p,dtype=float)
        for i in range (n):
            for j in range (p):
                self.mat_p[i][j]= self.mat_p[i][j]/d
        return None

    def cherche(self,ps):
        """
        Cherche le sous-marin
        Args:
            ps (float) : Correspond ├á la probabilit├⌐ que le senseur trouve le sous marin
            si celui-ci se trouve en position self.pos
        """
        cpt=0
        
        while(True):
            cpt+=1
            (i,j) = np.unravel_index(np.argmax(self.mat_p), self.mat_p.shape)
            if (i,j)==self.pos:
                k = random.random()
                if k < ps:
                    print("Senseur trouv├⌐ en pos "+ str((i,j)))
                    return cpt
            self.mat_p = self.mat_p / (1 - self.mat_p[i][j]*ps)
            self.mat_p[i][j] *= 1-ps

#s = Senseur(5,5,0)
#print(s.cherche(0.1))
