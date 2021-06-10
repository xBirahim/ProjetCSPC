"""
Gestionnaire de billes
"""

from multiprocessing import Process, Value, Lock, current_process
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
    identite = current_process().name  #getpid()

    for i in range(besoin):
        demander(besoin, identite)
        sleep(randint(0, 1))
        rendre(besoin, identite)

    fin = time()
    print(f"{identite} HAVE FINISHED IN {int(fin - debut)} s")
    sys.exit(0)


def controleur(nombre):
    with mutex:
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

    with mutex:
        print(f"{identite} wants {nombre} | {ressources.value} left")

    loop = True

    while loop:

        with mutex:
            if nombre <= ressources.value:
                loop = False
                print(f"{identite} finished waiting")
                print(f"\t{identite} | {nombre} / {ressources.value}")
                print(f"\t{identite} : Mutex Lock")
                ressources.value -= nombre

                print(f"\t{identite} <= {nombre} | {ressources.value}")

                print(f"\t{identite} : Mutex release\n")


def rendre(nombre, identite):

    print(f"{identite} : Mutex lock")

    mutex.acquire()
    ressources.value += nombre
    print(f"{identite} : Mutex release")
    print(f"{identite} => {nombre} | {ressources.value} now")
    mutex.release()


if __name__ == '__main__':
 
    mutex = Lock()
    n = 3
    max_ressources = 15
    ressources = Value('i', max_ressources)

    # Creation des processus

    processus = [Process(target=travailleur) for i in range(n)]

    for process in processus:
        process.start()
    for process in processus:
        process.join()
