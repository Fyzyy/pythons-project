import numpy as np
import matplotlib.pyplot as plt
from math import *

#Question 1
def rp(x,p):
    e = ceil(log(abs(x),10))
    return round(x, -(e-1)+p-1)

def print_test_q1():
    nb1 = 3.141592658
    nb2 = 10507.1823
    nb3 = 0.0001857563
    p1 = 4
    p2 = 6
    print("Début test q1")
    print(rp(nb1, p1))
    print(rp(nb2, p1))
    print(rp(nb3, p1))
    print()
    print(rp(nb1, p2))
    print(rp(nb2, p2))
    print(rp(nb3, p2))
    print("Fin test q2")

#Question 2
def add_machine(x,y,p):
    new_x = rp(x,p)
    new_y = rp(y,p)
    return rp(new_x + new_y,p)

def times_machine(x,y,p):
    new_x = rp(x,p)
    new_y = rp(y,p)
    return rp(new_x*new_y,p)

def print_test_q2():
    nb1 = 3.141592658
    nb2 = 10507.1823
    nb3 = 0.0001857563
    p1 = 4
    p2 = 6
    print("Début test q2")
    print(add_machine(nb1,nb2,p1), times_machine(nb1, nb2,p1))
    print()
    print(add_machine(nb1,nb2,p2), times_machine(nb1, nb2,p2))
    print("Fin test q2")
    
#Question 3
    
def relativ_error_add(x,y,p):
    return abs((x + y) - add_machine(x,y,p))/abs(x+y)
#Question 4
def relativ_error_times(x,y,p):
    return abs((x * y) - times_machine(x,y,p))/abs(x * y)

def print_test_q3_q4():
    nb1 = 3.141592658
    nb2 = 10507.1823
    nb3 = 0.0001857563
    p1 = 4
    p2 = 6
    print("Début test q3_q4")
    print(relativ_error_add(nb1,nb2,p1), relativ_error_times(nb1,nb2,p1))
    print()
    print(relativ_error_add(nb1,nb2,p2), relativ_error_times(nb1,nb2,p2))
    print("Fin test q3_q4")
    
#Question 5

def array_add_error(x,tab,p):
    return [relativ_error_add(x,k,p) for k in tab]

def array_times_error(x,tab,p):
    return [relativ_error_times(x,k,p) for k in tab]

def print_test_q5():
    p1, p2 = 4, 6
    x = 0.03184
    val_y = np.arange(-15, 15, 0.0001)
    val_error_add = array_add_error(x,val_y,p1)
    val_error_times = array_times_error(x,val_y,p1)
    # print(max(val_error_add))
    print(max(val_error_times))
    # plt.plot(val_y,val_error_add)
    plt.plot(val_y,val_error_times)
    plt.legend(["Multiplication"])
    # plt.legend(["Addition"])
    plt.xlabel("y")
    plt.ylabel("Erreur relative")
    plt.title("Erreur relative pour x = 0.03184 en fonction de y.")
    plt.show()