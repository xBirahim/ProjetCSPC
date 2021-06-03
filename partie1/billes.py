"""
Gestionnaire de billes
"""

from multiprocessing import Process, Value, Lock
from random import randint
from time import sleep
from os import getpid


def travailleur():
    """
    Faire un timer, un compteur de demandes aussi
    :return:
    """
    besoin = randint(1, 10)
    identite = getpid()

    for i in range(besoin):
        demander(identite)
        sleep(randint(2, 10))
        rendre()

    print(f"Le processus {identite} à fini son travail")

def controleur():

    if 0 < ressources.value <= max_ressources:
        return True
    else:
        return False

def demander(nombre, identite):
    """
    La fonction check s'il y a assez de billes pour le processus qui l'appelle
    Rajouter en arguments PID,
    et afficher "Le processus {PID} à demander {ressource} ressources / {ressources.value} restantes"
    :param nombre:
    :return:
    """

    #Mettre un while
    if nombre <= ressources.value:
        ressources.value -= nombre

    else:
        print("Pas assez de ressources")


def rendre(nombre, identite):
    pass


if __name__ == '__main__':
    n = 4
    max_ressources = 8
    ressources = Value('i', max_ressources)


    #Creation des processus

    for i in range(n):
        processus = [Process(target=travailleur) for i in range(n)]

    print(processus)
