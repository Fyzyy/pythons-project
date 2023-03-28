import math

from partie1 import *

def calclog(m:int, p:int, croissant:bool):
    sum = 0
    l = [*range(1,m)]

    if not croissant:
      l.reverse()

    for n in l:
        sum = rp(sum +((-1)**(n+1))/n ,p)
    return sum


def ln(x):
    k = 0
    y = 0
    p = 1
    
    while (k <= 6):
        while (x >= p + p * 10**(-k)):
            y = y + log(1 + 10**(-k))
            p = p + p * 10**(-k)
        k = k + 1
    return y + (x/p-1)
  
def exp(x):
    k = 0
    y = 1
    
    while (k <= 6):
        while (x >= log(1 + 10**(-k))):
            x = x - log(1 + 10**(-k))
            y = y + y * 10**(-k)
        k = k + 1
    return y + y * x




"""Questions

1.Dans une calculatrice typique un nombre 'flottant' occupe 8 octets 
  de mémoire et se décompose en :
  - une mantisse constituée de 13 chiffres codés indépendamment sur
    4 chiffres binaires (on parle de Binaire Code Decimal ou BCD) 
  - un exposant (puissance de 10) éventuellement signé
  - le signe du nombre (et de l'exposant s'il n'est pas signé)

    AVANTAGES : On ne stocke que sur 8 octets et nous n'avons pas besoin d'une grosse précision sur des calculatrices de base

    INCONVENIENTS : On ne peut pas faire de gros calculs à cause de la mentisse de 13 chiffres et ca nous apporte une perte de précision.

2. La technique générale pour réaliser les 4 algorithmes est d'utiliser une interpolation linéaire voir un développement en série.
On réduit au fur et à mesure l'intervalle de valeur servant à l'interpolation qui se rapproche de plus en plus de la valeur réelle de x.
Pour se faire, on dispose de 2 tableaux contenants des valeurs précalculées de l'inverse de la fonction exponentielle (Logartihme népérien) et un tableau de fonction atan.

Cette technique est efficace car elle ne necessite qu'un tableau avec quelques valeurs de la fonction.

  """

