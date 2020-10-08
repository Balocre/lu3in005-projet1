from code import *
import numpy as np

g1 = np.matrix([[0,0],[0,0]])
g2 = np.matrix([[0,0],[0,0]])

print("g1 == g2? {}".format(eq(g1,g2)))

g1 = np.matrix([[0,0],[0,0]])
g2 = np.matrix([[1,0],[0,0]])

print("g1 == g2? {}".format(eq(g1,g2)))

g1 = np.matrix([[0,0],[0,0]])
g2 = np.matrix([[0,0],[0,0],[0,0]])

print("g1 == g2? {}".format(eq(g1,g2)))

affiche(genere_grille())

print(nb_pos(genere_grille(),1))

r = plateau
place(r,1,(0,5),1)
place_alea(r,3)
place_alea(r,3)
place_alea(r,3)
print(r)

print(nb_pos_list(genere_grille(),[1,1]))

print("nb comp {}".format(comp_alea_grille(genere_grille())))

print("approx grilles {}".format(approx_total_grille(10)))

