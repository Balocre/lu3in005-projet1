from code import *
import unittest

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
            self.assertEqual(self.bataille_init.joue( (1, 2) ), 4)
            with self.assertRaises(ValueError):
                self.bataille_init.joue( (-1, -1) )
        


if __name__ == '__main__':
    unittest.main()