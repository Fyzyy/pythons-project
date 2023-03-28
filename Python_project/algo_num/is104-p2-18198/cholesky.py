import numpy as np
from scipy.linalg import lu

def cholesky_factorization(A):
    n = A.shape[0]
    L = np.zeros((n, n))
    for i in range(n):
        for j in range(i+1):
            s = np.dot(L[i,:j], L[j,:j])
            if (i == j):
                L[i,j] = np.sqrt(A[i,i] - s)
            else:
                L[i,j] = (1.0 / L[j,j] * (A[i,j] - s))
    return L

def generate_spd_cmatrix(n, density):
    A = np.zeros((n,n))
    for i in range(n):
        for j in range(i, n):
            if i==j:
                while A[i,j] == 0:
                    A[i,j] = np.random.normal(0,1)
            if np.random.uniform(0,1) < density:
                A[i,j] = np.random.normal(0,1)
                A[j,i] = A[i,j]
    return np.dot(A,A.T)

def cholesky_incomplete(A):
    n = A.shape[0]
    L = np.zeros((n,n))
    for i in range(n):
        for j in range(i, n):
            s = sum(L[i,k] * L[j,k] for k in range(j))
            if i == j:
                L[i,j] = np.sqrt(np.abs(A[i,i] - s))
            else:
                L[j,i] = (A[i,j] - s) / L[i,i]
    return L

def test_chol():
    A = np.array([[4, 12, -16], 
                  [12, 37, -43], 
                  [-16, -43, 98]])
    L = cholesky_factorization(A)
    print("Factorization de Cholesky: \n")
    print("Vérification: ", np.allclose(np.dot(L, L.T),A))

    M = np.dot(np.linalg.inv(L).T, np.linalg.inv(L))

    print("Verification qualité conditionnement: ", np.linalg.cond(np.dot(M,A))<np.linalg.cond(A))

def test_chol_incomplete():
    A = generate_spd_cmatrix(3, 0.5)
    L = cholesky_incomplete(A)

    print("\ntest_chol_incomplete :\n")
    # Test 1: Verification of symmetry
    print("triangulaire inf :",np.allclose(L, np.tril(L)))

    # Test 2: Verification of isometry
    print("multiplication = original :",np.allclose(np.dot(L, L.T), A))

    # Test 3: Verification of positive definiteness
    print("définie positive :",np.all(np.diag(L) > 0))

    M = np.dot(np.linalg.inv(L).T, np.linalg.inv(L))

    # Test 4: Verification of cond
    print("Verification qualité conditionnement: ", np.linalg.cond(np.dot(M, A))<np.linalg.cond(A))



