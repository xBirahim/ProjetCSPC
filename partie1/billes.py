"""
Gestionnaire de billes
"""

from multiprocessing import Process, Value, Lock
from random import randint
from time import sleep, time
from os import getpid
import sys


def travailleur():
    """
    Faire un timer, un compteur de demandes aussi
    :return:
    """
    debut = time()
    besoin = randint(1, max_ressources)
    identite = getpid()

    for i in range(besoin):
        demander(besoin, identite)
        sleep(randint(1, 2))
        rendre(besoin, identite)

    fin = time()
    print(f"{identite} à fini son travail en {fin - debut} secondes")
    sys.exit(0)


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
    print(f"{identite} demande {nombre} ressource(s) | Il y'en a {ressources.value}")

    showmessage = True

    while nombre > ressources.value:

        if showmessage:
            print(f"Demande de {identite} refusée")
            showmessage = False
        """
        Le nombre de ressources n'est pas suffisant, alors le processus va attendre en boucle
        """
        continue

    if nombre <= ressources.value:
        mutex.acquire(1) #mutex=0
        ressources.value -= nombre
        mutex.release()

        print(f"{identite} a pris {nombre} ressource(s) | Il en reste {ressources.value}")


def rendre(nombre, identite):

    mutex.acquire(1)
    ressources.value += nombre
    mutex.release()

    print(f"{identite} dépose {nombre} ressource(s) | Il y'en a {ressources.value} maintenant")


if __name__ == '__main__':
    mutex = Lock()
    n = 3
    max_ressources = 8
    ressources = Value('i', max_ressources)


    #Creation des processus
    processus = [Process(target=travailleur) for i in range(n)]

    for process in processus: process.start()
    for process in processus: process.join()
