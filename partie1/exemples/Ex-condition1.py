# Mai 2021
# Ex Var cond
# Variable de Condition pour synchronizer des étapes d'une travail tels que
# certaines partie seront en parallèle mais d'autre séquentielles, même dans des processus séparés.

# Ici on lance 3 processus dont deux feront l'étape 2 mais doivent attendre que le 3e processus fasse l'étape_1
# d'abord puis les deux autres en parallèle effectuent l'étape2.
import multiprocessing
import time

def etape_1(cond):
    """Première étape d'un travail puis notification à etape_2 de continuer"""
    name = multiprocessing.current_process().name
    print ('Lancement étape_1', name)
    with cond:
        print ("%s : étape_1 terminée; les process de l'étape 2 peuvent commencer" % name)
        cond.notify_all()

def etape_2(cond):
    """Attendre la  condition qui dit :  etape_1 terminée"""
    name = multiprocessing.current_process().name
    print ('Lancement étape_2', name)
    with cond:
        cond.wait()
        print ('%s en cours' % name)

if __name__ == '__main__':
    condition = multiprocessing.Condition()
    s1 = multiprocessing.Process(name='étape_1', target=etape_1, args=(condition,))
    s2_clients = [
        multiprocessing.Process(name='etape_2[%d]' % i, target=etape_2, args=(condition,))
        for i in range(1, 3)
        ]

    for c in s2_clients:
        c.start()
        time.sleep(1)
    s1.start()

    s1.join()
    for c in s2_clients:
        c.join()
        
"""
Lancement étape_2 etape_2[1]
Lancement étape_2 etape_2[2]
Lancement étape_1 étape_1
étape_1 : étape_1 terminée; les process de l'étape 2 peuvent commencer
etape_2[1] en cours
etape_2[2] en cours
"""