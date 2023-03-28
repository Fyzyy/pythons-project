import numpy as np

couleurs = ['green', '#FE1B00', 'yellow', 'black','#F4661B','#DEB887','blue','cyan']
                   
class Zone :
    def __init__(self):
        self._C = 0
        self._statut = 'vide'
        
    def set_normal(self):
        self._statut = 'population'
        
    def set_C(self,Tinf):
        self._C = Tinf
        self._statut = 'C'
        
    def set_mort(self):
        self._C = -1
        self._statut= 'mort'
        
    def est_C(self):
        if self._C >= 1:
            return True
        elif self._C <=0:
            return False
        return False
    
    def est_mort(self):
        if self._C == -1:
            return True
        else:
            return False
        
    def set_gueri(self):
        self._C = -2
        self._statut = 'gueri'
    
    def est_gueri(self):
        if self._statut == 'gueri':
            return true
        else:
            return false
    
    
    def print_couleur(self,Tinf):
        if self._C >= int(0.75*Tinf):
            return couleurs.index('yellow')
        elif self._C >= int(0.5*Tinf):
            return couleurs.index('#F4661B')
        elif self._C >=int(0.25*Tinf):
            return couleurs.index('#FE1B00')
        elif self._C == -1:
            return couleurs.index('black')
        elif self._C == -2:
            return couleurs.index('cyan')
        elif self._statut == 'population':
            return couleurs.index('green')
        else:
            return couleurs.index('#DEB887')
                                  