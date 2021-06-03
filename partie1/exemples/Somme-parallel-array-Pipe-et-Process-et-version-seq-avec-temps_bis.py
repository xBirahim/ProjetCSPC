# Nov 2020, CPE concurrent Python
# Exemple du cours 
# Somme parallèle avec fork d'abor
# Ici  somme avec "array" + Pipe (pas "Array" mais "array" comme numpy)
"""
Extrait doc Python sur mp.Pipe() :
Note that data in a pipe may become corrupted if two processes (or threads) try to read from or write 
to the same end of the pipe at the same time. Of course there is no risk of corruption from processes 
using different ends of the pipe at the same time.
"""
import array
import os, time
import multiprocessing as mp # pour Value, Pipe 

# La fonction des pour_fils_to_send
def somme(num_process, table, debut, fin_exclue, pour_fils_to_send) :
    # On enlève print du tableau, il est trop grand
    print("Je suis le pour_fils_to_send num ", num_process, "et je fais la somme du tableau de taille ", fin_exclue-debut)
    S_local=0
    for i in range(debut, fin_exclue) :
        S_local += tableau[i]
    
    pour_fils_to_send.send(S_local) # Non bloquant
    pour_fils_to_send.close()
    print(f"le pour_fils_to_send num {num_process}, envoie par send {S_local}")
    
if __name__ == "__main__" :
    taille = 10**6
    
    # Plus efficace que les listes
    tableau = array.array('i',[i for i in range(taille)])
    
    pour_pere_to_receive, pour_fils_to_send=mp.Pipe()
     
    deb=time.time()
    process1 = mp.Process(target=somme,args=(1, tableau, 0, taille // 2, pour_fils_to_send,))
    process2 = mp.Process(target=somme,args=(2, tableau, taille // 2, taille,pour_fils_to_send,))
    
    process1.start(); process2.start()

    moitie1=pour_pere_to_receive.recv() # Blocks until there is something to receive.
    moitie2=pour_pere_to_receive.recv()

    # On laisser "join" mais inutile dans ce cas car "recv()" est bloquant et les pour_fils_to_send terminent 
    # avec send (non bloquants)
    process1.join(); process2.join()
    
    fin=time.time()
    print("La somme totale du tableau obtenue : ", moitie1+moitie2, " en ", (fin-deb)*1000000)
    print(f"On vérifie que la somme par Python : {sum(tableau)}")
    
    #-------------------------------------------------------------------
    print('-'*50)
    print("Version séquentielle (avec pipe): ")
    deb=time.time()
    somme(1, tableau, 0, taille // 2,  pour_fils_to_send)
    somme(2, tableau, taille // 2, taille, pour_fils_to_send)
    moitie1=pour_pere_to_receive.recv() # Blocks until there is something to receive.
    moitie2=pour_pere_to_receive.recv()
    fin=time.time()
    print("La somme totale du tableau en version séquentielle : ", moitie1+moitie2, " en ",  (fin-deb)*1000000)
"""
e suis le pour_fils_to_send num  1 et je fais la somme du tableau de taille  500000
Je suis le pour_fils_to_send num  2 et je fais la somme du tableau de taille  500000
le pour_fils_to_send num 1, envoie par send 124999750000
le pour_fils_to_send num 2, envoie par send 374999750000
La somme totale du tableau obtenue :  499999500000  en  252648.11515808105
On vérifie que la somme par Python : 499999500000
--------------------------------------------------
Version séquentielle (avec pipe): 
Je suis le pour_fils_to_send num  1 et je fais la somme du tableau de taille  500000
le pour_fils_to_send num 1, envoie par send 124999750000
Je suis le pour_fils_to_send num  2 et je fais la somme du tableau de taille  500000
le pour_fils_to_send num 2, envoie par send 374999750000
La somme totale du tableau en version séquentielle :  499999500000  en  465073.1086730957

"""
    
"""
TRACE :
array('i', [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
Je suis le pour_fils_to_send num  1 et je fais la somme du tableau  array('i', [0, 1, 2, 3, 4])
le pour_fils_to_send num 1, envoie par send 10
Je suis le pour_fils_to_send num  2 et je fais la somme du tableau  array('i', [5, 6, 7, 8, 9])
le pour_fils_to_send num 2, envoie par send 35
La somme totale du tableau oobtenue :  45
On vérifie que la somme par Python : 45
"""
"""
if __name__ == "__main__" :
    taille=11
    arr1 = array.array('i', [1 for i in range(taille)])
    #arr2 = array.array('i', [0] * 10)
    pour_pere_to_receive.send_bytes(arr1)
    count = pour_fils_to_send.recv_bytes_into(arr2)
    assert count == len(arr1) * arr1.itemsize
    arr2
    #array('i', [0, 1, 2, 3, 4, 0, 0, 0, 0, 0])
    
    from multiprocessing import Process, Pipe
    
    def f(conn):
        conn.send([42, None, 'hello'])
        conn.close()
    
    if __name__ == '__main__':
        parent_conn, child_conn = Pipe()
        p = Process(target=f, args=(child_conn,))
        p.start()
        print(parent_conn.recv())   
        p.join()
"""
