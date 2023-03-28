import numpy as np

def make_H(U,V):
    n = np.shape(U)[0]
    N = (U-V)/np.linalg.norm(U-V)
    return np.eye(n)-2*np.dot(N,N.T)

def householder_product_vector(N,X):
    return X-(2*np.dot(N,np.dot(N.T,X))/np.linalg.norm(N)) #Complexité linéaire car on calcule d'abord N.T*U donc on ne fait apparaitre que des vecteurs

def householder_product_matrice(N,M):
    return M-(2*np.dot(N,np.dot(N.T,M))/np.linalg.norm(N))


def bidiagonal_QR(A):
    m, n = np.shape(A)
    Q = np.eye(m)
    R = np.copy(A)
    
    for k in range(n):
        x = R[k:m, k]
        
        x[0] = np.sign(x[0])*np.linalg.norm(x)

        R[k:m, k:n] = householder_product_matrice(x,R[k:m, k:n])

        Q[k:m, :] =  householder_product_matrice(x,Q[k:m, :])
    
    return Q, R



def test_qr():
    A = np.array([[1,2,0],
                  [2,5,6],
                  [0,1,9]])
    Q_ref,R_ref = np.linalg.qr(A)
    Q,R = bidiagonal_QR(A)
    print(np.dot(Q,R))
    print(np.allclose(Q,Q_ref) and np.allclose(R,R_ref))
    




def test_householder():
    
    U=np.array([[3],[4],[0]])
    V=np.array([[0],[0],[5]])
    N = (U-V)/np.linalg.norm(U-V)
    H_ref = np.array([[0.64, -0.48, 0.6], [-0.48, 0.36, 0.8], [0.6, 0.8, 0]])
    H = make_H(U,V)
    print("test_makeH:",np.allclose(H,H_ref))
    print("test mult:",np.allclose(householder_product_vector(N,U),V))

    M=np.array([[3,4,6],[4,0,8],[0,3,9]])
    #print(householder_product_matrice(N,M))

