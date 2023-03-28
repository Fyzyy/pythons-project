import numpy as np
import matplotlib.pyplot as plt
from decomposition import SVD

def compress(A, r):
    U,S,V = SVD(A)
    if (r > min(S.shape[0],S.shape[1])):
        print("rang r plus important que la taille de la matrice")
        exit()

    for i in range(r+1, min(S.shape[0],S.shape[1])): #check shape[0]
        S[i,i] = 0


    return np.dot(U, np.dot(S,V))

#transforme un matrice d'une image [[[r,g,b],...]] en[[r,g,b,...]]. 
def unpack(M):
    new_M = np.zeros((M.shape[0], M.shape[1]*3))
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            for color in range(3):
                new_M[i,j+color] = M[i,j][color] 
    return new_M

#transforme un matrice d'une image [[r,g,b,...]] en [[[r,g,b],...]]. 
def repack(M):
    new_M = np.zeros((M.shape[0], int(M.shape[1]/3), 3))
    for i in range(M.shape[0]):
        for j in range(int(M.shape[1]/3)):
            for color in range(3):
                new_M[i,j][color] = M[i,j+color]
    return new_M

def diff(A, k):
    B = compress(A, k)
    distance = 0
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            distance += abs(A[i,j,:].sum() - B[i,j,:].sum())

    return distance


def only_one_color(M, color_index):
    new_M = np.zeros((M.shape[0], M.shape[1]))
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            # print("at",i,j,"converted",M[i,j], "into", M[i,j][0])
            new_M[i,j] = M[i,j][color_index]
    return new_M

def add_color_channel(M, C, color):
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            M[i,j][color] = C[i,j]

    return M


def test_compress():
    img_full = plt.imread("p3_takeoff_base.png")
    # img_full = plt.imread("cat.png")
    n, m, colors = img_full.shape
    print(n,m,colors)
    # img_flat = unpack(img_full)
    # print(img_flat.shape)
    # img_base = repack(img_flat)
    # print(img_base.shape)

    minium_size = min(n,m)
    colors = [0,1,2]
    img_compress = np.zeros((minium_size, minium_size, len(colors)))

    for color in colors:
        one_colored = only_one_color(img_full, color)
        size = min(one_colored.shape[0], one_colored.shape[1])
        one_colored = one_colored[:size, :size]
        one_colored = compress(one_colored, 10)
        img_compress = add_color_channel(img_compress, one_colored, color)

    plt.imshow(img_compress)
    plt.show()

    # distances = []
    # max_rank = 20
    # for i in range(max_rank, 1, -5):
    #     distances.append(diff(img_compress, i))
    
    # print(distances)