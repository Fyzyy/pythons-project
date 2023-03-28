from Population2 import population
import numpy as np    
import matplotlib.pyplot as plt
import PIL.Image as Image



def perco(x,y,N,pr,d,Tinf,taux_mort = 0.1):
    F = 1
    G = 0
    H = 0
    Moy =[]
    X1 = []
    Y1,Y2,Y3,Y4 = [],[],[],[]
#    fig1 , ax1 = plt.subplots()
    fig2 , ax2 = plt.subplots()
    #fig3 , ax3 = plt.subplots()
    pop = x*y
    p = 1 - pr
    R0 = pr*7*d/100                  
    #print('R0 =', R0 )
    #calcul_proba(p)
    c = 1
    simulation = population(x,y,p)
    simulation.generer_population(d)
    simulation.generer_C(int(x/2),int(y/2),Tinf)
    simulation.graph_population(Tinf) #etat initial
    for k in range (N):
        #simulation.graph_population(Tinf,k) #toutes les étapes
        #print(k)
                
        f,g,h =  simulation.actu_zone(taux_mort,Tinf) #extraction
        F += f
        G += g          #cumul
        H += h
        moy = (F+f-G-H)/F
        X1.append(k)
        Y1.append((F-G-H)/pop) #case contamine 
        Y2.append(G/pop)       #gueri
        Y3.append(H/pop)       #mort
        Y4.append(1-(F)/pop)   #sain
        Moy.append(moy)
    
    #courbe
#    ax1.plot(X1,Y1,label='contamination',color = 'orange')
#    ax1.set_title("modèle percolation ("+"p="+str(pr)+",d="+str(d)+", m="+str(taux_mort)+")")
#    ax1.plot(X1,Y2, label = 'gueri',color  = 'green')
#    ax1.plot(X1,Y4 , label = 'suceptible', color = 'blue')
#    ax1.legend()
#    ax2.plot(X1,Moy)
    #print(Moy[0])
    
    #simulation.graph_population(Tinf) #juste derniere étape
    
    #expression regression exponentielle
    a,b = np.polyfit(X1,np.log(Moy),1)
    print("R = "+str(np.exp(b))+"*"+ str(np.exp(a))+"^n")
    
    #courbe
    Rsim = []
    for i in range(len(X1)):  #courbe théorique
        Rsim.append(np.exp(b)*(np.exp(a))**X1[i])
    ax2.plot(X1,Rsim, label = 'régression')
    
    return F
            
        
def calcul_proba(p):
    for i in range (9):
        print(i,1-p**i)

    
def p(dmin,dmax,dpas): #liste des densités ou y'a perco pour une proba donnée
    X = []
    for i in range(dmin,dmax,dpas):
        if perco(100,100,50,50,200,1,i):
            X.append(i)
    return X


#print(p(10,70,5))

def test_proba(p,d,n): #proportion moyennes sur n simulation
    c = 0
    for i in range(n):
        if perco(200,200,100,100,50,p,d,0,3): #changez les valeurs ici
            c += 1
    return c
        

def test_proba_li(lip,lid,n):
    f = open('donne.csv','w')
    for p in lip:
        for d in lid:
            c = test_proba(p,d,n)/n
            f.writelines(str(p) +';'+ str(d)+';'+ str(c)+'\n')
            print(p,d,c)
    f.close()

def dens_crit(p):
    I = []
    X = [k for k in range(100)]
    for d in X:
        print(d)
        I.append(perco(60,60,60,p,d,4))
    plt.plot(X,I,label = 'densité critique'+'p ='+ str(p))
    return I    
    
def moy_dens_crit(p,N):        
    J = np.zeros(100)
    X = [k for k in range(len(J))]
    for i in range(N):
        print(i)
        J += np.array(dens_crit(p),dtype = np.float32)
    plt.plot(X,J/N,label = 'densité critique'+'p ='+ str(p))
    


dens_crit(0.25)

#perco(x,y,N,pr,d,Tinf,taux_mort = 0.1)
#perco(100,100,90,0.4,70,4)
    











