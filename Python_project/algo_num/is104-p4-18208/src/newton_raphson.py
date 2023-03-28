import numpy as np

def F(X:np.ndarray):
    return np.array([[X[0]**2],
                     [X[1]+X[0]],
                     [X[1]-2*X[0]]])

def df(f:callable, i:int, X:np.ndarray, h:int=0.01):
    new_X1 = np.zeros(X.shape)
    new_X2 = np.zeros(X.shape)

    new_X1[i] = X[i]+h
    new_X2[i] = X[i]-h
    print(((f(new_X1)-f(new_X2))/(2*h)))
    return ((f(new_X1)-f(new_X2))/(2*h))



def Jac(f:callable, X:np.ndarray):
    n, m = np.shape(X)[0], np.shape(f(X))[0]
    return np.array([[df(f, i, j, X)] for i in range(n) for j in range(m)]).reshape(n,m).T


def test_F():
    X_test = np.array([1,1])
    #print(F(X_test))
    #print(df(F,0,0,X_test))

    Jac(F,X_test)


test_F()