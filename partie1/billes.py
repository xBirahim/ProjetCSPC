"""
Gestionnaire de billes
"""

from multiprocessing import Process, Value, Lock, Semaphore
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
    besoin = randint(1, 4)
    identite = getpid()

    for i in range(besoin):
        demander(besoin, identite)
        sleep(randint(0, 1))
        rendre(besoin, identite)

    fin = time()
    print(f"{identite} à fini son travail en {fin - debut} secondes")
    sys.exit(0)


def controleur():

    if 0 <= ressources.value <= max_ressources:
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
    print(f"debut de demander pour {identite}")
    print(f"{identite} demande {nombre} ressource(s) | Il y'en a {ressources.value}")

    showmessage = True


    while nombre > ressources.value:
 
        if showmessage:
            print(f"Demande de {identite} refusée")
            showmessage = False
        """
        Le nombre de ressources n'est pas suffisant, alors le processus va attendre en boucle
        """

    print(f"fin attente pour {identite}")


    

    if nombre <= ressources.value:
        print(f"{identite} | {nombre} / {ressources.value}")

        mutex.acquire()
        print(f"mutex pris par {identite}")
        ressources.value -= nombre

        print(f"{identite} a pris {nombre} ressource(s) | Il en reste {ressources.value}")
        mutex.release()
        print(f"mutex déposé par {identite}")


def rendre(nombre, identite):

    print(f"mutex pris par {identite}")

    mutex.acquire()
    ressources.value += nombre
 
    print(f"mutex déposé par {identite}")

    print(f"{identite} dépose {nombre} ressource(s) | Il y'en a {ressources.value} maintenant")
    mutex.release()



if __name__ == '__main__':
 
    mutex = Lock()
    n = 3
    max_ressources = 3
    ressources = Value('i', max_ressources)


    #Creation des processus
    processus = [Process(target=travailleur) for i in range(n)]

    for process in processus: process.start()
    for process in processus: process.join()
