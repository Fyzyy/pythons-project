import numpy as np
import matplotlib.pyplot as plt

#from partie1 import newton_raphston

def norme(vector:np.ndarray)->float:
    return (np.sum(vector**2))**.5

def barycenter(positions:np.ndarray, masses:np.ndarray=np.array([[1]]))->np.ndarray:
    """
    Returns the barycenter of masses located at positions.

    Example :
    a = np.array([[0, 0],
                [1, 0]])
    b = np.array([[1],
                [0.01]])
    \>>>barycenter(a, b)\n
    array([0.00990099, 0.        ])

    :param positions: The positions of the masses.
    :param masses: The masses (must have the same length as positions). Defaults to 1 for all the masses.
    :return: The barycenter of the masses in a np.ndarray.
    """
    if len(masses) != len(positions) and masses == np.array([1]):
        masses = np.array([[1]*len(positions)])

    return np.sum(positions*masses, axis=0)/np.sum(masses)

def f_elastic(k:float, pos:np.ndarray, pos0:np.ndarray = np.array([0, 0], dtype="float64"))->np.ndarray:
    """
    Returns the elastic force applied to an object at the pos position from a spring which origin is pos0 and spring constant is k.
    :param k: The spring constant.
    :param pos: The position of the object affected by the elastic force.
    :param pos0: The origin of the elastic force.
    :return: The elastic force in a np.ndarray.
    """
    return -k*(pos-pos0)

def f_centri(k:float, pos:np.ndarray, pos0:np.ndarray = np.array([0, 0], dtype="float64"))->np.ndarray:
    """
    Returns the centrifugal force applied to an object at the pos position by a centrifugal force which origin is pos0 and intensity is k.
    :param k: The intensity of the force.
    :param pos: The position of the object affected by the centrifugal force.
    :param pos0: The origin of the centrifugal force.
    :return:The centrifugal force in a np.ndarray.
    """
    return k*(pos-pos0)

def f_gravit(k:float, pos:np.ndarray, pos0:np.ndarray= np.array([0, 0], dtype="float64"))->np.ndarray:
    """
    Returns the gravitational force applied to an object at the pos position from a mass located at pos0 and mass is k.
    :param k: The mass of the mass.
    :param pos: The position of the object affected by the gravitational force.
    :param pos0: The mass creating the gravitational force.
    :return: The gravitational force in a np.nd.array.
    """
    if (pos==pos0).all():
        return np.zeros(pos.shape)
    coefficient:float = (np.sum((pos-pos0)**2))**1.5
    return -k/coefficient*(pos-pos0)

def sum_f(pos:np.ndarray)->np.ndarray:
    brcenter = barycenter(np.array([[0, 0], [1, 0]]), np.array([[1], [0.01]]))
    def mass1(position):
        return f_gravit(1, position, np.array([0, 0]))

    def mass2(position):
        return f_gravit(0.01, position, np.array([1, 0]))

    def centri(position):
        return f_centri(1, position, brcenter)

    return mass1(pos)+mass2(pos)#+centri(pos)

x_start, x_end, x_numbers = -1.5, 1.5, 1000
y_start, y_end, y_numbers = -1, 1, 1000
x_center = (x_start+x_end)/2
y_center = (y_start+y_end)/2
x = np.linspace(x_start, x_end, x_numbers)
y = np.linspace(y_start, y_end, y_numbers)
print(x)
print(y)
forces = np.zeros((x_numbers, y_numbers), dtype="float64")

for i in range(x_numbers):
    for j in range(y_numbers):
        forces[i, j] = norme(sum_f(np.array([x[i], y[j]])))

forces = np.log10(forces)

plt.imshow(forces, origin="lower")
print(forces)
plt.colorbar()
plt.title("Champ de force (norme)")
plt.xlabel("x entre {} et {}".format(x_start, x_end))
plt.ylabel("y entre {} et {}".format(y_start, y_end))
plt.show()
print(sum_f(np.array([1.5, 0])))