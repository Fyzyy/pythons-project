import numpy as np
import math
import pylab as plt
import gradient as gr 
import cholesky as ch


def genA(N):
    A=np.eye(N*N,N*N)*(-4)
    h= 1/(N+1)
    for i in range(0,N*N):
        if(i+1<N*N):
            if((i+1)%N != 0):
                A[i,i+1]=1
        if(i-1>=0):
            if(i%N != 0):
                A[i,i-1]=1
        if(i-N>=0):
            A[i,i-N]=1
        if(i+N<N*N):
            A[i,i+N]=1
    return (1/h**2)*A

def MtoV(M): #Transfome une matrice de dimension (n,n) en un vecteur de taille (n*n) 
    N=np.shape(M)[0]
    V=np.zeros((N*N,1))
    for j in range(0,N):
        for i in range(0,N):
            V[i+j*N]=M[j,i]
    return V

def VtoM(V): #Transfome un vecteur de taille (n*n) en une matrice de dimension (n,n)
    N=int(math.sqrt(V.size))
    M=np.zeros((N,N))  
    for j in range(0,N):
        for i in range(0,N):
            M[j,i]=V[i+j*N]
    return M

def resolve_heat(source):
    N = np.shape(source)[0]
    A = genA(N)
    source = MtoV(source)
    T0 = np.zeros((N*N,1))

    #wihtout precond
    T1,i1 = gr.conjgrad(A,source,T0,verbose=True)

    #precond
    L = ch.cholesky_incomplete(A)
    M = np.dot(np.linalg.inv(L).T, np.linalg.inv(L))
    T2,i2 = gr.precond_conjgrad(A, source, T0, M,verbose=True)


    return VtoM(T1).T, VtoM(T2).T,i1,i2

def show(T): #Affiche la diffusion thermique
    plt.imshow(T,cmap='hot',interpolation='bicubic')
    plt.show()





