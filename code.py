import random

map = [] #map 2D
for i in range(10):
    map.append([0]*10)
dict_bateau = dict() #dictionnaire de bateaux
dict_bateau = {1:5, 2:4,3:3,4:3,5:2}

def peut_placer(grille,bateau,position,direction):
    """[summary]

    Args:
        grille (int[][]): map 2D 10x10
        bateau (String): nom du bateau
        position ((int,int)): position dans la matrice 
        direction (int): 1 pour horizontal, 2 pour vertical

    Returns:
        [type]: [description]
    """
    (k,l) = position
    i=k
    j=l
    if (direction == 1):
        while (j<10 and j < l + dict_bateau[bateau]):
            if grille[i][j]!=0:
                return False
            j=j+1
    else :
        while (i<10 and i < l + dict_bateau[bateau]):
            if grille[i][j]!=0:
                return False
            i=i+1
    return True

def place(grille,bateau,position,direction):
    (k,l) = position
    i=k
    j=l
    if (peut_placer(grille,bateau,position,direction)):
        if (direction == 1):
            while (j<10 and j < l + dict_bateau[bateau]):
                grille[i][j]=bateau
                j=j+1
        else :
            while (i<10 and i < l + dict_bateau[bateau]):
                grille[i][j]=bateau
                i=i+1
        return True
    return False

def place_alea(grille,bateau):
    b=False
    while not b:
        position = (random.randint(0,9),random.randint(0,9))
        direction = random.randint(1,2)
        print("position : "+ position)
        print("direction : "+ direction)
        b = place(grille,bateau,position,direction)
    return

place(map,1,(0,0),1)
place_alea(map,3)
place_alea(map,3)
place_alea(map,3)
for i in range(10):
    print(map[i])
print ("testok")