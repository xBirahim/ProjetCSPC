from multiprocessing import Lock, Process, Value
from os import getpid
from time import sleep
from random import randint
import sys

def personne():

    temps = randint(3, 5)
    litre = randint(1, 10)

    identite = getpid()

    print(f"{identite} arrive devant les toilettes !")

    mutex.acquire()
    print(f"{identite} à pris la clé des toilettes")

    sleep(1)
    print(f"{identite} est rentré dans les toilettes")
    sleep(temps)
    valeur.value += litre

    print(f"{identite} à lâcher {litre} | il y a maintenant {valeur.value} dans le reservoir")

    mutex.release()
    print(f"{identite} est sorti des toilettes après {temps} secondes")


    sys.exit(0)



if __name__=='__main__':

    mutex = Lock()
    valeur = Value('i', 0)
    personnes = [Process(target=personne) for i in range(8)]


    for i in personnes: i.start()

    for i in personnes: i.join()