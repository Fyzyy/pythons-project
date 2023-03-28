import numpy as np
import matplotlib.pyplot as plt
import householder

def invariant_BD(M):

    n,m = np.shape(M)
    diag = np.diagonal(M)
    diag_sup = np.diagonal(M, offset=1)
    mask = M - (np.diag(diag) + np.diag(diag_sup,k=1))
    return np.allclose(mask,np.zeros((n,m)))


def bidiag_qr(A):
    # A est la matrice à décomposer
    n, m = np.shape(A)
    # Initialisation des matrices Qleft, Qright et BD
    Qleft = np.eye(n)
    Qright = np.eye(n)
    BD = A
    for i in range(n):
        # Calcul de la matrice de Householder Q1 pour BD[i:n,i]
        u = BD[i:, i]
        u[0] += np.sign(u[0]) * np.linalg.norm(u)
        u /= np.linalg.norm(u)
        Q1 = np.eye(n)
        Q1[i:, i:] -= 2 * np.outer(u, u.T)
    
        # Mise à jour de BD et de Qleft
        BD = Q1 @ BD
        Qleft = Qleft @ Q1
        
        if i != m-2:
            # Calcul de la matrice de Householder Q2 pour BD[i,(i+1):m]
            v = BD[i, i+1:]
            v[0] += np.sign(v[0]) * np.linalg.norm(v)
            v /= np.linalg.norm(v)
            Q2 = np.eye(n)
            Q2[i+1:, i+1:] -= 2 * np.outer(v, v.T)
            
            # Mise à jour de BD et de Qright
            BD = BD @ Q2
            Qright = Q2 @ Qright

    # Retourne les matrices Qleft, BD et Qright
    return Qleft, BD, Qright



def SVD(BD,Nmax=100):
    S = BD
    n,m = np.shape(S)
    U = np.eye(n)
    V = np.eye(n)

    for i in range(Nmax):
        Q1,R1 = np.linalg.qr(S.T)
        Q2,R2 = np.linalg.qr(R1.T)
        #Q1,R1 = qr_decomposition(S.T)
        #Q2,R2 = qr_decomposition(R1.T)
        S = R2
        #assert(invariant_BD(S) and invariant_BD(R1) and invariant_BD(R2))
        U = np.dot(U,Q2)
        V = np.dot(Q1.T,V)
    return U,S,V



def genererBidiagonaleAleatoire(n):
    D1 = np.random.rand(n)
    D2 = np.random.rand(n-1)
    return np.diag(D1) + np.diag(D2, k=1)

def dessinerConvergenceDiagS(n, step=50, precision = 10**-7):
    BD = genererBidiagonaleAleatoire(n)
    y = np.zeros(step)
    for i in range(step):
        res = SVD(BD, i)
        S = res[1]
        y[i] = np.count_nonzero(np.abs(S.diagonal(offset=1)) > precision)
    x = np.arange(step) + 1
    plt.plot(x, y)
    plt.xlabel("Nombre d'étapes")
    plt.ylabel("Nombre d'éléments extradiagonaux de S")
    plt.title("Convergence de la décomposition SVD par QR")
    plt.show()

def invariant_SVD(BD):
    U,S,V = SVD(BD)
    return np.allclose(np.dot(U,np.dot(S,V)),BD) 


def test_bidiag_qr():
    A = np.array([[1,2,3],
                  [4,5,6],            
                  [7,8,9]])
    Qleft, BD, Qright = bidiag_qr(A)
    np.allclose(np.dot(Qleft,np.dot(BD,Qright)),A)



def test_SVD():

    BD = np.array([[1,2,0],
                   [0,2,1],
                   [0,0,3]])
    
    U,S,V = SVD(BD)
    print("U*S*V=BD:",np.allclose(np.dot(U,np.dot(S,V)),BD))
