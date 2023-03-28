import numpy as np
import matplotlib.pyplot as plt 

#---------définition des constantes-----------

beta1= 0.03 # en 1/jour
gamma1= 0.01 # en 1/jour 
beta2=4.56 # en 1/mois (donée caractérisant la peste Eyam)
gamma2=2.78 # en 1/ mois (donnée caractérisant la peste Eyam)

#------définitions des fonctions--------------

def f(x,t):
    return x*t

def h(t,a,tau):
    return a*t/(a*t+tau)

def Euler(F,X0,tf,n):
    dt = tf/n
    T=np.linspace(0,tf,n+1) 
    Y=np.zeros((len(T),len(X0)))
    Y[0]=X0
    for i in range(len(T)-1):
        Y[i+1] = Y[i]+dt*F(Y[i],T[i])
    return T,Y
    
def SIS(X,t):
    Y=np.zeros(len(X))
    Y[0] = -beta1*X[0]*X[1] + gamma1*X[1]
    Y[1] = beta1*X[0]*X[1] - gamma1*X[1]
    return Y


def SISh(X,t):
    Y=np.zeros(len(X))
    Y[0] = -(1-h(t,0.02,1)/2)*beta1*X[0]*X[1] + gamma1*X[1]
    Y[1] = (1-h(t,0.02,1)/2)*beta1*X[0]*X[1] - gamma1*X[1]
    return Y
    
def SIR(X,t):
    Y=np.zeros(len(X))
    Y[0] = -beta2*X[0]*X[1]
    Y[1] = beta2*X[0]*X[1] - gamma2*X[1]
    Y[2] = gamma2*X[1]
    return Y

def tracé(X0,tf,n):
    fig,ax=plt.subplots(1,2,figsize=(18,8))
    T1,Y1=Euler(SISh,X0,tf,n)
    T2,Y2=Euler(SIS,X0,tf,n)
    S1= Y1[:,0:1]
    I1= Y1[:,1:2]
    S2= Y2[:,0:1]
    I2= Y2[:,1:2]

    fig,ax=plt.subplots(1,2,figsize=(18,8))

    ax[0].set_title("modèle SISh")
    ax[0].plot(T1,S1)
    ax[0].plot(T1,I1)

    ax[1].set_title("modèle SIS")
    ax[1].plot(T2,S2)
    ax[1].plot(T2,I2) 

def trace2(X0,tf,n):
    
    fig,ax=plt.subplots(figsize=(12,8))
    T1,Y1=Euler(SIR,X0,tf,n)
    T2=np.arange(0,4.5,0.5)
    
    S= Y1[:,0:1]
    I= Y1[:,1:2]
    R= Y1[:,2:3]
    S2=np.array([254/261,235/261,201/261,153.5/261,121/261,108/261,97/261,float("nan"),83/261])
    I2=np.array([7/261,14.5/261,22/261,29/261,20/261,8/261,8/261,float("nan"),0])
    
    plt.plot(T1,S, label=("S(t)"))
    plt.plot(T1,I, label="I(t)")
    plt.plot(T1,R, label="R(t)")
    plt.plot(T2,S2,"o",label="proportion de suscpetibles (données historiques)")
    plt.plot(T2,I2,"o",label="proportion d'infectés (données historiques)")
    plt.legend()
    plt.title("modèle SIR de la peste d'Eyam")
    plt.xlabel("temps en mois")
    

def SIRRetard(X,XRetard,t):
    Y=np.zeros(len(X))
    Y[0] = -beta2*X[0]*XRetard[1]
    Y[1] = beta2*X[0]*XRetard[1] - gamma2*X[1]
    Y[2] = gamma2*X[1]
    
    return Y

def EulerRetard(F,X0,p,tf,n):
    dt = tf/n
    T=np.linspace(0,tf,n+1) 
    Y=np.zeros((len(T),len(X0)))
    Y[0]=X0
    for i in range(len(T)-1):
        if i <= p:
            Y[i+1] = X0
        else:
            Y[i+1] = Y[i]+dt*F(Y[i],T[i])
    return T,Y











# T1,X1=Euler(SIS,np.array([0,1]),500,1000) 
# S1=X1[:,0:1]
# I1=X1[:,1:2]

# T2,X2=Euler(SIS,np.array([0.2,0.8]),500,1000) 
# S2=X2[:,0:1]
# I2=X2[:,1:2]

# T3,X3=Euler(SIS,np.array([0.5,0.5]),500,1000) 
# S3=X3[:,0:1]
# I3=X3[:,1:2]

#T4,X4=Euler(SIS,np.array([0.99,0.01]),500,1000) 
#S4=X4[:,0:1]
#I4=X4[:,1:2]


# fig,ax=plt.subplots(figsize=(12,8))
# plt.plot(T1,S1,label="S(t) avec S(0)=0")
# plt.plot(T1,I1,label="I(t) avec I(0)=1")
# plt.plot(T2,S2,label="S(t) avec S(0)=0.2")
# plt.plot(T2,I2,label="I(t) avec I(0)=0.8")
# plt.plot(T3,S3,label="S(t) avec S(0)=0.5")
# plt.plot(T3,I3,label="I(t) avec I(0)=0.5")
#plt.plot(T4,S4,label="S(t) avec S(0)=0.99")
#plt.plot(T4,I4,label="I(t) avec I(0)=0.01")
#plt.legend()
#plt.title("beta=0.03 jour^-1 ; gamma=0.01 jour^_1")
#plt.xlabel("temps en jours")
#plt.show() 
trace2([254/261,7/261,0],5,50)