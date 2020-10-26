from code import *
import unittest
import numpy as np

class TestPartie1(unittest.TestCase):

    def setUp(self):
        self.bateaux = {1:5, 2:4, 3:3, 4:3, 5:2}

        self.grille_vierge = np.zeros( (10,10) )

        self.grille = np.zeros( (10, 10) )
        self.grille[1, 2:5] = 4
        self.grille[3, 3:7] = 2
        self.grille[5:8, 4] = 3
        self.grille[7:9, 1] = 5
        self.grille[5:10, 9] = 1
        #[[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        # [0, 0, 4, 4, 4, 0, 0, 0, 0, 0],
        # [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        # [0, 0, 0, 2, 2, 2, 2, 0, 0, 0],
        # [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        # [0, 0, 0, 0, 3, 0, 0, 0, 0, 1],
        # [0, 0, 0, 0, 3, 0, 0, 0, 0, 1],
        # [0, 5, 0, 0, 3, 0, 0, 0, 0, 1],
        # [0, 5, 0, 0, 0, 0, 0, 0, 0, 1],
        # [0, 0, 0, 0, 0, 0, 0, 0, 0, 1]]

    def test_peut_placer(self):
        self.assertTrue(peut_placer(self.bateaux, self.grille_vierge, 1, (2, 2), "+x"))
        self.assertFalse(peut_placer(self.bateaux, self.grille_vierge, 1, (10, 10), "+y"))
        self.assertFalse(peut_placer(self.bateaux, self.grille, 1, (5, 9), "+x"))

    def test_place(self):
        self.assertEqual(place(self.bateaux, self.grille_vierge, 1, (0, 0), "+x"), ((0, 0), (1, 0), (2, 0), (3, 0), (4, 0)))
        self.assertIsNone(place(self.bateaux, self.grille, 1, (0, 3), "+x"))

    def test_place_alea(self):
        self.assertFalse(place_alea(self.bateaux, self.grille_vierge, 1))

    def test_affiche(self):
        affiche(self.grille)
    
    def test_eq(self):
        self.assertFalse(eq(self.grille, self.grille_vierge))
        self.assertTrue(eq(self.grille, self.grille ))

        with self.assertWarns(Warning):
           eq(self.grille, np.zeros( (1, 1) ))

    def test_genere_grille(self):
        genere_grille(self.bateaux)

class TestBataille(unittest.TestCase):

    def setUp(self):
        self.bateaux = {1:5, 2:4, 3:3, 4:3, 5:2}

        self.grille = np.zeros( (10,10) )

        self.grille[1, 2:5] = 4
        self.grille[3, 3:7] = 2
        self.grille[5:8, 4] = 3
        self.grille[7:9, 1] = 5
        self.grille[5:10, 9] = 1
        #[[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        # [0, 0, 4, 4, 4, 0, 0, 0, 0, 0],
        # [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        # [0, 0, 0, 2, 2, 2, 2, 0, 0, 0],
        # [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        # [0, 0, 0, 0, 3, 0, 0, 0, 0, 1],
        # [0, 0, 0, 0, 3, 0, 0, 0, 0, 1],
        # [0, 5, 0, 0, 3, 0, 0, 0, 0, 1],
        # [0, 5, 0, 0, 0, 0, 0, 0, 0, 1],
        # [0, 0, 0, 0, 0, 0, 0, 0, 0, 1]]

        self.bataille_random = Bataille(self.bateaux)

        self.bataille_init = Bataille(self.bateaux, self.grille)

    def test_joue(self):
        self.assertNotEqual(self.bataille_init.grille[1][2], self.bataille_init.grille_decouverte[1][2])
        self.assertEqual(self.bataille_init.joue( (1, 2) ), 4)
        self.assertEqual(self.bataille_init.grille[1][2], self.bataille_init.grille_decouverte[1][2])

        self.assertIsNone(self.bataille_init.joue( (0, 0) ))

        with self.assertRaises(ValueError):
            self.bataille_init.joue( (-1, -1) )
    
    def test_victoire(self):
        self.assertFalse(self.bataille_init.victoire())
        for i in range(0, 10):
            for j in range(0, 10):
                self.bataille_init.joue( (i, j) )
        self.assertTrue(self.bataille_init.victoire())

class TestJourAlea(unittest.TestCase):
    
    def setUp(self):
        self.bateaux = {1:5, 2:4, 3:3, 4:3, 5:2}

        self.grille = np.zeros( (10, 10) )
        self.grille[1, 2:5] = 4
        self.grille[3, 3:7] = 2
        self.grille[5:8, 4] = 3
        self.grille[7:9, 1] = 5
        self.grille[5:10, 9] = 1
        #[[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        # [0, 0, 4, 4, 4, 0, 0, 0, 0, 0],
        # [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        # [0, 0, 0, 2, 2, 2, 2, 0, 0, 0],
        # [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        # [0, 0, 0, 0, 3, 0, 0, 0, 0, 1],
        # [0, 0, 0, 0, 3, 0, 0, 0, 0, 1],
        # [0, 5, 0, 0, 3, 0, 0, 0, 0, 1],
        # [0, 5, 0, 0, 0, 0, 0, 0, 0, 1],
        # [0, 0, 0, 0, 0, 0, 0, 0, 0, 1]]

        self.joueur_alea = JoueurAlea(Bataille(self.bateaux, self.grille))

    def test_joue(self):
        pos_jouee = self.joueur_alea.joue()
        self.assertIsInstance(pos_jouee, tuple)
        print("Le joueur à joué en position : {}".format(pos_jouee))

    def test_epuisement(self):
        print("Liste des coups joués par le joueur aléaoire")
        while c := self.joueur_alea.joue():
            print("{}".format(c))

        self.assertTrue(self.joueur_alea.bataille.victoire())

class TestJoueurHeur(unittest.TestCase):

    def setUp(self):
        self.bateaux = {1:5, 2:4, 3:3, 4:3, 5:2}

        self.grille = np.zeros( (10, 10) )
        self.grille[1, 2:5] = 4
        self.grille[3, 3:7] = 2
        self.grille[5:8, 4] = 3
        self.grille[7:9, 1] = 5
        self.grille[5:10, 9] = 1
        #[[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        # [0, 0, 4, 4, 4, 0, 0, 0, 0, 0],
        # [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        # [0, 0, 0, 2, 2, 2, 2, 0, 0, 0],
        # [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        # [0, 0, 0, 0, 3, 0, 0, 0, 0, 1],
        # [0, 0, 0, 0, 3, 0, 0, 0, 0, 1],
        # [0, 5, 0, 0, 3, 0, 0, 0, 0, 1],
        # [0, 5, 0, 0, 0, 0, 0, 0, 0, 1],
        # [0, 0, 0, 0, 0, 0, 0, 0, 0, 1]]

        self.joueur_heur = JoueurHeur(Bataille(self.bateaux, self.grille))

    def test_joue(self):
        pos_jouee = self.joueur_heur.joue()
        self.assertIsInstance(pos_jouee, tuple)
        print("Le joueur à joué en position : {}".format(pos_jouee))

    def test_epuisement(self):
        print("Liste des coups joués par le joueur aléaoire")
        while c := self.joueur_heur.joue():
            # affiche(self.joueur_heur.bataille.grille_decouverte)
            print("{}".format(c))

        self.assertTrue(self.joueur_heur.bataille.victoire())

class TestJoueurProba(unittest.TestCase):

    def setUp(self):
        self.bateaux = {1:5, 2:4, 3:3, 4:3, 5:2}

        self.grille = np.zeros( (10, 10) )
        self.grille[1, 2:5] = 4
        self.grille[3, 3:7] = 2
        self.grille[5:8, 4] = 3
        self.grille[7:9, 1] = 5
        self.grille[5:10, 9] = 1
        #[[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        # [0, 0, 4, 4, 4, 0, 0, 0, 0, 0],
        # [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        # [0, 0, 0, 2, 2, 2, 2, 0, 0, 0],
        # [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        # [0, 0, 0, 0, 3, 0, 0, 0, 0, 1],
        # [0, 0, 0, 0, 3, 0, 0, 0, 0, 1],
        # [0, 5, 0, 0, 3, 0, 0, 0, 0, 1],
        # [0, 5, 0, 0, 0, 0, 0, 0, 0, 1],
        # [0, 0, 0, 0, 0, 0, 0, 0, 0, 1]]

        self.joueur_proba = JoueurProba(Bataille(self.bateaux, self.grille))

    def test_joue(self):
        pos_jouee = self.joueur_proba.joue()
        self.assertIsInstance(pos_jouee, tuple)
        print("Le joueur à joué en position : {}".format(pos_jouee))

    def test_epuisement(self):
        print("Liste des coups joués par le joueur aléaoire")
        while c := self.joueur_proba.joue():
            affiche(self.joueur_proba.bataille.grille_decouverte)
            print("{}".format(c))

        self.assertTrue(self.joueur_proba.bataille.victoire())

if __name__ == '__main__':
    unittest.main()