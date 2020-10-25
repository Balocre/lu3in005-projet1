from code import *
import numpy as np

bateaux = {1:5, 2:4, 3:3, 4:3, 5:2}

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

# print("nb comp {}".format(comp_alea_grille(genere_grille())))

# print("approx grilles {}".format(approx_total_grille(10)))

for i in range(1, 6):
    affiche(genere_mat_proba(bateaux[i]))

affiche(genere_mat_proba(4, (2,2)))

t = genere_mat_proba(5)
max_p = np.unravel_index(np.argmax(t, axis=None), t.shape)
print("max_p = ({})".format(max_p))

print("test : {}".format(t[(1,1)]))


m = ()

for taille_bat in range(2, 6):
    m += (genere_mat_proba(taille_bat),)

    t = OrderedDict()
    for x, y in [ pos for pos in itr.product(range(10), range(10)) ]:
        t[(x, y)] = [p[x][y] for p in m]


    t = SortedDict(lambda x: np.sum(x), t)

    print("{}".format(list(t)[0]))
    print("{}".format(list(t)[1]))
    print("=====================")
    
while t:
    print("{}".format(np.sum(t.popitem()[1])))

for b in bateaux.keys():
    print("{}".format(b))

m = dict( map( lambda k : (k, genere_mat_proba(bateaux[k])), bateaux.keys() ) )

print("{}".format(m))
