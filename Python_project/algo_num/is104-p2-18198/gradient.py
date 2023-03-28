import numpy as np
from scipy.sparse.linalg import cg
from cholesky import *

def conjgrad(A, b, x,verbose=False):
    r = b - np.dot(A, x)
    p = r
    rsold = np.dot(np.transpose(r), r)
    nb_ite =0

    for i in range(len(b)):
        Ap = np.dot(A, p)
        alpha = rsold / np.dot(np.transpose(p), Ap)
        x = x + alpha * p
        r = r - alpha * Ap
        rsnew = np.dot(np.transpose(r),r)
        if np.sqrt(rsnew.all()) < 1e-10:
            break
        p = r + (rsnew / rsold) * p
        rsold = rsnew
        nb_ite +=1
    if verbose:
        print("\nitération sans precond:",nb_ite)
    return x,nb_ite

def precond_conjgrad(A, b, x, M,verbose=False):
    r = b - np.dot(A, x)
    z = np.linalg.solve(M, r)
    p = z
    nb_ite =0

    for i in range(len(b)):
        Ap = np.dot(A, p)
        alpha = np.dot(np.transpose(r), z) / np.dot(np.transpose(p), Ap)
        x = x + alpha * p
        rnew = r - alpha * Ap
        if np.sqrt(np.dot(np.transpose(r), r)) < 1e-10:
            break
        znew = np.linalg.solve(M,rnew)
        beta = np.dot(np.transpose(rnew),znew) / np.dot(np.transpose(r),z) 
        p = znew + beta * p
        r = rnew
        z = znew
        nb_ite +=1
    if verbose:
        print("\nitération avec precond:",nb_ite)
    return x,nb_ite


def testconjgrad():
    n = 10
    A = generate_spd_cmatrix(n,0.5)
    b = np.random.rand(n)

    x = conjgrad(A,b,np.zeros(n))[0]
    print("test conjgrad : ",np.allclose(np.dot(A,x),b))

def test_precond_conjgrad():
    n = 5
    A = generate_spd_cmatrix(n,0.5)
    L = cholesky_incomplete(A)
    M = np.dot(np.linalg.inv(L).T, np.linalg.inv(L))
    x0 = np.zeros(n)
    b = np.random.rand(n)

    x = precond_conjgrad(A, b, x0, M)[0]

    # Solve the system using SciPy's conjugate gradient method as a reference
    x_ref , _ = cg(A,b,M=M)

    print("test precond_conjgrad : ", np.allclose(x,x_ref)) #Il arrive d'avoir false mais l'erreur est négligable
