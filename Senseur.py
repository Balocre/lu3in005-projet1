import random
import numpy as np


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