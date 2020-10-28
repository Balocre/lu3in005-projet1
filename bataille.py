import random
import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import itertools as itr
import warnings
from typing import Optional
from typing import Tuple
from typing import Union
import math

#Constantes
N = 10
#Dictionnaire reliant les differents bateaux et leur taille en nombre de case
bateaux = {1:5, 2:4, 3:3, 4:3, 5:2}

#Représentation du plateau vide en tant que matrice 10x10
plateau = np.zeros( (10,10) )

# Partie 1

def peut_placer(bateaux, grille, id_bat, pos, direction):
    """Teste s'il est possible de placer un bateau sur la grille de jeu.

    Args:
        bateaux (dict of int: int): Dictionnaire associant chaque bateau à sa taille.
        grille (int[][]): Matrice représentant la grille de jeu.
        id_bat (int): Id du bateau.
        position (int*int): Position de l'origine du bateau dans la grille de jeu.
        direction (String): Direction en fonctions des axes x (vertical) et y (horisontal) \"+x\" pour horizontal-droite, \"+y\" pour vertical-bas.

    Returns:
        bool: True si le bateau peut être placé, False sinon.
    """

    x, y = pos

    directions = frozenset(["+x", "+y"])
    if direction not in directions: raise ValueError("{} n'est pas une direction valide".format(direction))

    x, y = pos
    taille_bat = bateaux[id_bat]

    if (x < 0) or (y < 0) or (x + taille_bat > N) or (y + taille_bat > N): return False # on vérifie que les coordonées sont dans la grille

    if (direction == "+y"):
       if not np.any(grille[x, y:y+taille_bat]): return True # on vérifie que les cases de la grille sont libres

    elif (direction == "+x"):
       if not np.any(grille[x:x+taille_bat, y]): return True
    
    return False

def place(bateaux, grille, id_bat, pos, direction) -> Optional[Tuple[Tuple[int, int], ...]]:
    """Place un bateau sur la grille de jeu si c'est possible.

    Args:
        bateaux (dict of int: int): Dictionnaire associant chaque bateau à sa taille.
        grille (int[][]): Matrice représentant la grille de jeu.
        id_bat (int): Id du bateau.
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


def place_alea(bateaux, grille, id_bat):
    """Place un bateau à une position aléatoire de la grille de jeu

    Args:
        bateaux (dict of int: int): Dictionnaire associant chaque bateau à sa taille.
        grille (int[][]): Matrice représentant la grille de jeu.
        bateau (int): Id du bateau.

    Returns:
        tuple(tuple()): Tuple de coordonées
    """

    while r := not place(bateaux, 
        grille, 
        id_bat, 
        (random.randint(0, 9), random.randint(0, 9)), 
        random.sample( frozenset(["+x", "+y"]), 1)[0]
        ):
        continue

    return r


def affiche(grille, ax=None):
    """Affiche l'état de la grille de jeu.
    
    Args:
        grille (int[][]): Matrice représentant la grille de jeu.
        ax (matplolib.axex): Axe sur lequel dessiner la figure si fournis
    """

    close = 0

    if not ax:
        fig = plt.figure()
        plt.matshow(grille)
        plt.waitforbuttonpress()
        plt.close(fig)
    else :
        cmap = cm.tab10
        cmap.set_bad('r')
        cmap.set_under('k')
        ax.matshow(grille, cmap=cmap, vmin=0, vmax=9)
        plt.draw()
        plt.waitforbuttonpress()
        ax.clear()

def eq(grille_a, grille_b):
    """Compare 2 grilles pour l'égalité.
    
    Args:
        grille_a (int[][]): Matrice représant la première grille de jeu.
        grille_b (int[][]): Matrice représant la deuxième grille de jeu.

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
        bateaux (dict of int: int): Dictionnaire associant chaque bateau à sa taille.
        n (int): Nombre d'itérations de comp_alea_grille à éffectuer.
    
    Returns:
        (int): La moyenne du nombre d'itérations éfféctuées.
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
        bateaux (dict of int: int): Dictionnaire associant chaque bateau à sa taille
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

    -On génère aléatoirement n grilles avec les 3 premiers bateaux.
    -On calcule exactement n fois le nombre de combinaisons des 2 bateaux restants sur ces grilles pour trouver la valeur moyenne.
    -Retourne la multiplication de cette moyenne par le nombre de combinaisons des 3 premiers bateaux sur une grille vide.
    Args:
        bateaux (dict of int: int): Dictionnaire associant chaque bateau à sa taille
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
    """Représente une partie de bataille navale

    Args:
        bateaux (dict of int: int): Dictionnaire associant chaque bateau à sa taille.
        grille (int[][]): Grille d'une batailel initialisée.


    Attributes:
        grille (int[][]): Matrice représentant la grille de jeu.
        grille_decouverte (int[][]): Matrice représentant la grille de jeu.
    """

    def __init__(self, bateaux, grille=None):
        if grille is not None: # dans le cas ou une grille est passée en paramètre la bataille se sjue sur cette grille
            self.grille = grille 
        else: # sinon génère une grille aléatoire
            self.grille = genere_grille(bateaux)

        # initialisation de la grille masquée, à chaque coup joué cette grille prend la valeure de la grille de jeu en la position du coup
        self.grille_decouverte = np.empty( (10, 10) )
        for i in range(10):
            for j in range(10):
                self.grille_decouverte[i][j] = -1

        # les bateaux qui sont encore en jeu
        self.bateaux = bateaux


    def joue(self, pos) -> Optional[Union[int, bool]]:
        """Joue un coup à la position pos

        Args:
            pos ((int, int)): La position à laquelle jouer le coup

        Returns:
            Optional[Union[int, bool]]: L'id du bateau coulé, True si le bateau est simplement touché, None si rien touché
        """

        (x, y) = pos

        if (x < 0) or (y < 0) or (x > 9) or (y > 9):
            raise ValueError("la position spécifiée n'est pas dans la grille de jeu")

        self.grille_decouverte[pos] = self.grille[pos] # on met à jour la carte masquée

        if self.grille[pos]: # si il y a un bateau ou le joueur vise
            return True

        for b, t in bateaux.copy().items(): # on parcours le dictionnaire des bateaux
            if np.sum(self.grille_decouverte == b) == t: # si la somme des éléments découverts correspondannt au bateau rdt égale à sa taille, \
                                                         # ça signifie que le bateau est coulé
                del self.bateaux[b] # on retire le bateau du dictionnaire
                print("Bateau {} trouvé".format(b))
                return b

        return None # la fonction indique que rien n'a été touché

    def victoire(self):
        """Vérifie si la partie est finie.

        Cette fonction compare la grille de jeu et la grille de découverte et si grille_decouverte == grille
        celà signifie que toutes les positions contenant des bateaux ont été jouées et par conséquent que
        la partie est finie.

        Returns:
            bool: True si la partie est finie, False sinon.
        """
        if not self.bateaux: # quand plus aucun bateau n'est en jeu
            return True
        return False

    def reset(self):
        pass
    
class Joueur:
    """Représente un joueur de bataille navale

    Args:
        bataille (Bataille): Bataille à laquelle le joueur participe.
        
    Attributes:
        bataille (Bataille): Bataille à laquelle le joueur participe.
        
    Note:
        Cette classe ne sert que de super classe pour les classes en héritant et ne doit pas être instanciée.
        Utiliser JoueurAlea, JoueurHeur ou JoueurProba.
    """

    def __init__(self, bataille=None):
        if bataille:
            self.participe(bataille)

    def joue(self):
        """Cette fonction vérifie si le joueur participe à une bataille

        Raises:
            AttributeError: Si le joueur ne participe pas à une bataille rase AtttibuteError car self.bataille n'éxiste pas
        """

        if not hasattr(self, 'bataille'): # si le joueur ne participe pas à une bataille son attribut bataille n'est pas initialisé
            raise AttributeError("Le joueur ne participe pas actuellement à une bataille")

    def participe(self, bataille):
        """Set la bataille à laquelle le joueur participe.

        Args:
            bataille (Bataille): Bataille à laquelle le joueur participe.
        """

        self.bataille = bataille
        print("Le joueur a rejoint la bataille {}".format(self.bataille))

class JoueurAlea(Joueur):
    """Représente un joueur ayant un comportement aléatoire.

    Args:
        bataille (Bataille): La bataille jouée par le joueur.

    Attributes:
        bataille (Bataille): La bataille jouée par le joueur.
        coup_prep (list((int, int))): Liste des coups préparés par le joueur.
            La liste de coup est mélangée après son instanciation.
    """

    def __init__(self, bataille=None):
        super().__init__(bataille)
        
    def participe(self, bataille):
        super().participe(bataille)

        # génère une liste de position aléatoires dans la grille
        self.coups_prep = list(itr.product(range(10), range(10))) 
        random.shuffle(self.coups_prep)

    def joue(self):
        """Joue un coup de la bataille de manière aléatoire.
        
        Pop un élément de la liste de coup et le joue sur la bataille.

        Returns:
            (int, int): La position du coup joué
        """

        super().joue()

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

    def __init__(self, bataille=None):
        super().__init__(bataille)
        self.coups_joue = dict() # ce dict contient la liste des coups joués, en utilisant pour clé le couple (x, y) représentant la position du coup 
                                 # et ayant pour valeur l'id du bateau trouvé à la position ou None

    def participe(self, bataille):
        super().participe(bataille)

        # XXX: utiliser un tuple comme valeur serait certainement plus rapide, dans ce cas corriger les index, mais dict beaucoup plus pratique
        # génère un dictionnaire qui contient la liste des coups préparés par le joueur
        self.coups_prep = dict(
            (pos, dict((b, 1) for b in self.bataille.bateaux.keys())) # 
            for pos in self.coups_prep) # en utilisant pour clé le couple (x, y) représentant la position du coup 
                                        # et ayant pour valeur un dict ayant pour clé les id des bateaux et valeur 1 si on peut trouver le bateau correspondant à la position 0 sinon 
        
    def joue(self):
        """Joue un coup de la bataille en utilisant une heuristique.

        L'heuristique est la suivante:
        Cherche une cible de manière aléatoire.
        Sur une touche :
            * Prioritise les cases adjacentes pour la recherche.
            * Si bateau touché dans une case ajacente explore l'axe formé par le coup actuel et le bateau touché à côté.
            * Limite la recherche à la taille max des bateaux encore en jeu.

        Returns:
            (int, int): La position du coup joué.
        """

        Joueur.joue(self) # pour le AttributeError si pas de bataille initialisée

        if not self.coups_prep: # ne devrait jamais arriver
            warnings.warn("Le joueur ne peux plus jouer, tout ses coups sont épuisés")
            return None

        x, y = self.coups_prep.popitem()[0]
        b = self.bataille.joue( (x, y) ) # si le coup touche

        if b:
            # on retire la possibilité de trouver b aux positions potentielles "plus loin" qu'une position ayant déjà étée jouée avec un autre bateau que b ait été découvert ou dont on à éliminé la possibilité de contenir b

            liste_prio = []
            axe = None
            direction = None

            # vérif si bateau touché dans case adjacente et si oui prioritise la recherche dans la direction opposée
            if self.coups_joue.get((x+1, y)):
                axe = 'x'
                direction = '-'
            if self.coups_joue.get((x-1, y)):
                axe = 'x'
                direction = '+'
            if self.coups_joue.get((x, y+1)):
                axe = 'y'
                direction = '-'
            if self.coups_joue.get((x, y-1)):
                axe = 'y'
                direction = '+'

            # taille max des bateaux encore en jeu
            maxb = max(self.bataille.bateaux.values())

            if axe == None or axe == 'y':
                # haut
                if direction == None or direction == '+':
                    for i in range(y-1, y-maxb, -1): # pour les positions n'ayant pas été jouées et ne pouvant pas contenir b et les position ayant été jouées et contenant un autre bateau que b
                        if (x, i) in self.coups_joue and self.coups_joue[(x, i)] != b:
                            break
                        elif (x, i) in self.coups_prep:
                            liste_prio.append((x, i))
                # bas
                if direction == None or direction == '-':
                    for i in range(y+1, y+maxb):
                        if (x, i) in self.coups_joue and self.coups_joue[(x, i)] != b:
                            break
                        elif (x, i) in self.coups_prep:
                            liste_prio.append((x, i))
                
                # si il n'y a pas assez d'espace en y pour placer le bateau
                if len(liste_prio) < maxb-1:
                    list_prio = []

            if axe == None or axe == 'x':
                # gauche
                if direction == None or direction == '+':
                    for j in range(x-1, x-maxb, -1):
                        if (j, y) in self.coups_joue and self.coups_joue[(j, y)] != b:
                            break
                        elif (j, y) in self.coups_prep:
                            liste_prio.append((j, y))
                # droite
                if direction == None or direction == '-':
                    for j in range(x+1, x+maxb):
                        if (j, y) in self.coups_joue and self.coups_joue[(j, y)] != b:
                            break
                        elif (j, y) in self.coups_prep:
                            liste_prio.append((j, y))
                
                # si il n'y à pas assez d'espace en x
                liste_prio_x = [(i ,j) for (i, j) in liste_prio if j == y]
                if len(liste_prio_x) < maxb-1:
                    liste_prio = [(i ,j) for (i, j) in liste_prio if i == x]

            # on augemente la priorité des coups sur les positions pouvant potentiellement contenir le bateau b dans la file i.e. une croix autours de la position du b touché
            for c in reversed(liste_prio):
                self.coups_prep[c] = self.coups_prep.pop(c) # on bouge les positions en fin du dict (elle seront donc appelées en premier sur un popitem)

        # TODO:
        # * arreter l'explo si coup dans le vide adjacent à bateau touché
        else:
            if self.coups_joue.get((x+1, y)):
                pass
            if self.coups_joue.get((x-1, y)):
                pass
            if self.coups_joue.get((x, y+1)):
                pass
            if self.coups_joue.get((x, y-1)):
                pass

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
        for i in range(max(x-taille_bat+1, 0), min(x+1, 10-taille_bat+1)):
            r[i:i+taille_bat, y] = [k+1 for k in r[i:i+taille_bat, y]]
        
        for j in range(max(y-taille_bat+1, 0), min(y+1, 10-taille_bat+1)):
            r[x, j:j+taille_bat] = [l+1 for l in r[x, j:j+taille_bat]]

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

    def __init__(self, bataille=None):
        super().__init__(bataille)

        self.coups_joue = dict()
        
    def participe(self, bataille):
        super().participe(bataille)
        
        # génère un dict associant chaque bateau à sa matrice de proba initiale
        m = dict( map( lambda k : (k, genere_mat_proba(self.bataille.bateaux[k])), self.bataille.bateaux.keys() ) )

        self.coups_prep = dict()
        for (x, y) in [ pos for pos in itr.product(range(10), range(10)) ]:
            self.coups_prep[(x, y)] = dict( map( lambda k: (k, m[k][x][y]), self.bataille.bateaux.keys() ) )

    def joue(self):
        """Joue un coup de la bataille parmis les coups ayant la plus grande proba de toucher un bateau

        Returns:
            (int, int): La position du coup joué.
        """

        Joueur.joue(self)

        if not self.coups_prep:
            warnings.warn("Le joueur ne peux plus jouer, tout ses coups sont épuisés")
            return None

        self.coups_prep = dict( sorted( self.coups_prep.items(), key=lambda x: sum(x[1].values() ) ) ) # on réorganise l'ordre du dictionnaire en fonction de la probabilité d'un coup de toucher un bateau

        x, y = self.coups_prep.popitem()[0]

        b = self.bataille.joue( (x, y) ) # si le coup touche
        
        if b and b is not True: # si le bateau est coulé
            for pos in self.coups_prep.copy():
                del self.coups_prep[pos][b] # on retire les entrées correspondant au proba de toucher le bateau sur les cases encore en jeu

            for pos in zip(*np.where(self.bataille.grille_decouverte == b)):
                self.coups_joue[pos] = b # on met à jour des cases ou le bateau à été découvert
            
            for pos, _ in filter(lambda e : e[1] == b, self.coups_joue.items()): # on itère sur les positions du bateau
                # pour chaque bateau encore en jeu on soustrait la matrice de proba générée sur les positions du bateau pour remettre la matrice de proba dans son état initiale (bateaux trouvés exclus)
                for bb in self.bataille.bateaux.keys():
                    mb = genere_mat_proba(self.bataille.bateaux[bb], pos)

                    for (i,j), p in self.coups_prep.items():
                        p[bb] -= self.bataille.bateaux[bb] * mb[i][j]
            

        elif b is True:
            for bb in self.bataille.bateaux.keys():
                mb = genere_mat_proba(self.bataille.bateaux[bb], (x, y))

                for (i,j), p in self.coups_prep.items():
                    p[bb] += self.bataille.bateaux[bb] * mb[i][j]
        
        else:
            for bb in self.bataille.bateaux.keys():
                mb = genere_mat_proba(self.bataille.bateaux[bb], (x, y))

                for (i,j), p in self.coups_prep.items():
                    p[bb] -= mb[i][j]

        self.coups_joue[(x, y)] = b

        return (x, y)

class Senseur():
    def __init__(self, n, p,repar):
        """
        Constructeur : initialise les dimensions, la matrice de probabilité et la repartition.
        Args :
            n (int) : nombre de lignes
            p (int) : nombre de colonnes
            repar (int) : repartition - 1 pour centree - 2 en bordure - 3 gauche nul - sinon aleatoire
        """
        mat_p = self.genere_mat_proba_senseur(n,p,repar) #matrice de probabilite
        self.place_senseur(n,p) #initialise l'attribut pos

    def place_senseur(self,n,p):
        """
        Initialise l'attribut pos qui correspond au tuple (i,j) représentant la position
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
        """Retourne une matrice de probabilité N*P selon une distribution repar.
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
            ps (float) : Correspond à la probabilité que le senseur trouve le sous marin
            si celui-ci se trouve en position self.pos
        """
        cpt=0
        
        while(True):
            cpt+=1
            (i,j) = np.unravel_index(np.argmax(self.mat_p), self.mat_p.shape)
            if (i,j)==self.pos:
                k = random.random()
                if k < ps:
                    print("Senseur trouvé en pos "+ str((i,j)))
                    return cpt
            self.mat_p = self.mat_p / (1 - self.mat_p[i][j]*ps)
            self.mat_p[i][j] *= 1-ps

#s = Senseur(5,5,0)
#print(s.cherche(0.1))

def partie(joueur):
    bataille = Bataille(bateaux, genere_grille(bateaux))
    joueur.participe(bataille)
    i = 0

    plt.matshow(joueur.bataille.grille)
    plt.waitforbuttonpress()

    plt.ion()

    if isinstance(joueur, JoueurProba):
            fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2)

    else :
        fig, ax1 = plt.subplots(nrows=1, ncols=1)

    while not joueur.bataille.victoire():
        
        affiche(joueur.bataille.grille_decouverte, ax1)
        
        if isinstance(joueur, JoueurProba):
            m = np.zeros((10, 10))
            for k in range(10):
                for l in range(10):
                    if((k, l) in joueur.coups_prep):
                        m[k][l] = sum(joueur.coups_prep[(k, l)].values())

            m = m/np.sum(m)

            ax2.matshow(m, cmap='gray')
            plt.draw()
        
        x, y = joueur.joue()
        
        print("Le joueur à joué en position ({}, {}):".format(x, y))
        
        grille_vise = joueur.bataille.grille_decouverte.copy()
        grille_vise[x][y] = np.nan
        
        affiche(grille_vise, ax1)
        del grille_vise

        i += 1

    
    print("Le joueur à fini la partie en {} coups".format(i))


def main():
    print(len(sys.argv))
    print("""Bienvenue dans le projet de bataille navale probabiliste de Ali Benabdallah et  Antoine Audras
Le code des fonctions se trouve à la racine du projet dans le fichier bataille.py
Un jeu de test écrit avec le framework unittest est disponible dans le dossier test
""")

    print("""Veuillez séléctioner un joueur à faire jouer :
1 - Joueur aléatoire
2 - Joueur heuristique
3 - Joueur probabiliste""")

    no_joueur = input("Votre choix : ")

    if no_joueur == "1":
        partie(JoueurAlea())
    elif no_joueur == "2":
        partie(JoueurHeur())
    elif no_joueur == "3":
        partie(JoueurProba())
    else:
        print("Votre séléction n'est pas valide")

if __name__ == "__main__":
    import sys
    main()