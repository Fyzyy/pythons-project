from Cellule2 import Zone,couleurs
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors

class population:
    def __init__(self,x,y,p):
        self._p = p
        self._x = x #taille en x de la zone
        self._y = y # taille en y de la zone
        self.zone = [[Zone() for y_zone in range (self._y)] for x_zone in range (self._x)]        
            
    def graph_population(self,Tinf): #dessine le graph de la zone
        #fig, ax = plt.subplots()
        cmap = colors.ListedColormap(couleurs)
        bound = [-0.5 + i for i in range(len(couleurs)+1)]
        norm = colors.BoundaryNorm(boundaries=bound, ncolors=len(couleurs))
        ligne=[]
        for x in self.zone:
            colone=[]
            for y in x:
                colone.append(y.print_couleur(Tinf))
            ligne.append(colone)
        #ax.imshow(np.array(ligne), cmap=cmap, norm=norm)
        

    def generer_population(self,d): #genere les cases d'individu 
        for x in range(len(self.zone)):
            for y in range(len(self.zone[x])):
                case=self.zone[x][y]
                if np.random.randint(0,100) >= 100-d :
                    case.set_normal()


    def generer_C(self,x,y,Tinf): #case de départ du virus
        start=self.zone[x][y]
        start._C = Tinf

                 
    def check_voisin(self,check_x,check_y): #donne liste de voisins
        livoisin=[]
        #print("zone cible",self)
        for i in range (-1,2):
            for j in range (-1,2):
                voisin_x = check_x + i
                voisin_y = check_y + j
                if (i,j)!=(0,0) and voisin_x >= 0 and voisin_y >= 0 and voisin_x <= (self._x-1) and voisin_y <= (self._y-1):
                    livoisin.append(self.zone[voisin_x][voisin_y])
        return livoisin    
    
        
    def tic_C(self): #retourne la liste des cases contaminé apres 1 itération
        mort=[]
        liC=[]
        for x in range(len(self.zone)):
            for y in range(len(self.zone[x])):
                cible = self.zone[x][y]
                if cible._C >= 1:
                   liC.append(cible)
        for zone in liC:
            zone._C += -1
            if zone._C == 0:
                mort.append(zone)
        return liC , mort
    
    def ignition(self,n): #proba de se faire contaminer
        if n ==0:
            return 0
        else:
            m=0
            for i in range (n):
                m = max(m,np.random.rand())
            return m
    
    def actu_zone(self,taux_mort,Tinf): #actualise toute la zone 1 fois
        C=[] #liste des cases qui vont se faire contaminer
        gueri = []
        mort1 = []
        liC, mort = self.tic_C() 
        for zone in mort:
            pmort = np.random.rand()
            if pmort < taux_mort:  
                zone.set_mort()
                mort1.append(zone)
            else:
                zone.set_gueri()
                gueri.append(zone)
                
        for x in range(len(self.zone)):
            for y in range(len(self.zone[x])):
                
                if self.zone[x][y]._statut == 'population':
                    livoisin = self.check_voisin(x,y) #attribue les voisins de la zone cible
                    nb_C=0
                    for zone_voisin in livoisin: #check etat des zones voisins
                        if zone_voisin.est_C(): # si contaminer alors ajoute a la liste
                            nb_C+=1  #liste des voisins contaminer de la zone

                    zone_cible = self.zone[x][y]
                    if zone_cible.est_C() == False : #si la zone n'est pas en contaminé
                        if self.ignition(nb_C) >= self._p : #probabilité que le virus se propage
                            C.append(zone_cible)
            
                    
        for zone in C:
            zone.set_C(Tinf)                       #contamine
        return len(C),len(gueri),len(mort1)       #retourne le nombre de case en contaminer,gueri,mort
        
        
    def check_fin(self): #verifie si c'est la fin
        x = self._x
        y = self._y
        for i in range (x-1): #vérifie si le bord est contaminer
            if self.zone[0][i].est_mort() or self.zone[i][0].est_mort() or self.zone[x-1][i].est_mort() or self.zone[i][x-1].est_mort() :
                return 'perco'
        for i in range(x): # vérifie si y'a au moins une case suseptible
            for j in range(y):
                if self.zone[i][j].est_C() == True :
                    return False
                elif i == x-1 and j ==y-1:
                    return 'fin'
        
        
                    
        