#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt 
from scipy.linalg import lstsq


def matrice_donnees_reelles(S,I):
    
    N=len(S)
    A=np.zeros((3*N,2))
    A[:N,0]=np.transpose(-S*I)
    A[N:2*N,0]=np.transpose(S*I)
    A[N:2*N,1]=np.transpose(-I)
    A[2*N:,1]=np.transpose(I)
    
    return A


def derivee(X,h):
    
    n=len(X)
    Y=np.zeros((n,1))
    Y[0,0]=(X[1,0]-X[0,0])/h
    for i in range(1,n-1):
        Y[i,0]=(X[i+1,0]-X[i-1,0])/2*h
    Y[n-1,0]=(X[n-1,0]-X[n-2,0])/h
    
    return Y


def Retablis(I): # on va considérer ici que les individus nouvellement infectés sont tous rétablis au bout de 1 semaine
    X=np.zeros((len(I),1))
    X[0,0]=0
    X[1,0]=I[0,0]
    for i in range (1,len(I)-1):
        X[i+1,0]=X[i,0]+I[i+1,0]      #les rétablis se cumulent car on considère qu'ils ne peuvent plus être malades
    return X


def Euler(F,X0,tf,n):
    dt = tf/n
    T=np.linspace(0,tf,n+1) 
    Y=np.zeros((len(T),len(X0)))
    Y[0]=np.transpose(X0)
    for i in range(len(T)-1):
        Y[i+1] = Y[i]+dt*np.transpose(F(Y[i],T[i]))
    return T,Y


def SIR(X,t):
    Y=np.zeros((len(X),1))
    Y[0] = -beta*X[0]*X[1]
    Y[1] = beta*X[0]*X[1] - gamma*X[1]
    Y[2] = gamma*X[1]
    return Y

def SIRRetard(X,XRetard,t):
    Y=np.zeros((len(X),1))
    Y[0] = -beta*X[0]*XRetard[1]
    Y[1] = beta*X[0]*XRetard[1] - gamma*X[1]
    Y[2] = gamma*X[1]
    return Y


def EulerRetard(f,X0,p,tf=500,n=1000):
    dt=tf/n
    T=np.linspace(0,tf,n+1)
    Y=np.zeros((len(T),len(X0)))
    Y[0]=np.transpose(X0)
    for i in range (len(T)-1):
        
        if i-p <= 0:
            Y[i+1]=np.transpose(X0)
        else:
            Y[i+1]=Y[i]+dt*np.transpose(f(Y[i],Y[i-p],T[i]))
    return T,Y



def trace(X0,tf,n):
    fig,ax=plt.subplots(figsize=(12,8))
    T1,Y1=EulerRetard(SIRRetard,X0,1,tf,n)#retard
    T3,Y3=Euler(SIR,X0,tf,n)
    T2=np.arange(0,35,1)       #35=len(I)=len(R)=len(S)
    S1= Y1[:,0:1]
    I1= Y1[:,1:2]
    R1= Y1[:,2:3]
    
    S3= Y3[:,0:1]
    I3= Y3[:,1:2]
    R3= Y3[:,2:3]
    
    plt.plot(T1,S1, label=("Sr(t)"), color = 'red' )
    plt.plot(T1,I1, label="Ir(t)", color = 'red')
    plt.plot(T1,R1, label="Rr(t)", color = 'red')
    
    plt.plot(T3,S3, label=("S(t)"), color = 'green')
    plt.plot(T3,I3, label="I(t)", color = 'green')
    plt.plot(T3,R3, label="R(t)", color = 'green')
    
    #plt.plot(T2,S,"o",label="proportion de susceptibles (données réelles)")
    #plt.plot(T2,I,"o",label="proportion d'infectés (données réelles)")
    #plt.plot(T2,R,"o",label='proportion de rétablis (issue des données réelles)')
    plt.legend()
    plt.title("modèle SIR de la Covid-19")
    plt.xlabel("temps en semaines")
    
    

Ibis=np.array([[5.96],[6.75],[10.05],[12.24],[16.9],[29.56],[53.58],[78.11],[95.94],[152.17],[181.46],[208.12],[254.39],[277.34],[307.36],[434.91],[466.51],[587.73],[625.85],[473.54],[259.29],[166.37],[126.22],[97.71],[88.3],[116.61],[157.15],[142.16],[140.07],[178.05],[184.85],[197.17],[210.03],[212.73],[253.32]]) #nouveaux individus infectés chaque semaine 
I=np.multiply(Ibis,1/10000) #ici j'ai du "tricher" car avec 100 000 les variations ne sont pas visibles (et les valeurs de Ibis sont pour 100 000 habitants) 
R=Retablis(I) 
pop=np.ones((len(Ibis),1))
S=pop-R-I


A=matrice_donnees_reelles(S,I)
Y=np.concatenate((derivee(S,1),derivee(I,1),derivee(R,1)))
X=lstsq(A,Y)
beta=X[0][0]
gamma=X[0][1]

print(beta)
print(gamma)
print(beta/gamma)

trace(np.array([S[0],I[0],R[0]]),35,100)




