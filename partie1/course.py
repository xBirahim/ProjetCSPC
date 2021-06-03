# Juin 2019
# Course hippique
# Version très basique, sans mutex sur l'écran, sans arbitre, sans annoncer le gagnant, ... ...
# Sans mutex écran

CLEARSCR="\x1B[2J\x1B[;H"        #  Clear SCReen
CLEAREOS = "\x1B[J"                #  Clear End Of Screen
CLEARELN = "\x1B[2K"               #  Clear Entire LiNe
CLEARCUP = "\x1B[1J"               #  Clear Curseur UP
GOTOYX   = "\x1B[%.2d;%.2dH"       #  Goto at (y,x), voir le code

DELAFCURSOR = "\x1B[K"
CRLF  = "\r\n"                  #  Retour à la ligne

# VT100 : Actions sur le curseur
CURSON   = "\x1B[?25h"             #  Curseur visible
CURSOFF  = "\x1B[?25l"             #  Curseur invisible

# VT100 : Actions sur les caractères affichables
NORMAL = "\x1B[0m"                  #  Normal
BOLD = "\x1B[1m"                    #  Gras
UNDERLINE = "\x1B[4m"               #  Souligné


# VT100 : Couleurs : "22" pour normal intensity
CL_BLACK="\033[22;30m"                  #  Noir. NE PAS UTILISER. On verra rien !!
CL_RED="\033[22;31m"                    #  Rouge
CL_GREEN="\033[22;32m"                  #  Vert
CL_BROWN = "\033[22;33m"                #  Brun
CL_BLUE="\033[22;34m"                   #  Bleu
CL_MAGENTA="\033[22;35m"                #  Magenta
CL_CYAN="\033[22;36m"                   #  Cyan
CL_GRAY="\033[22;37m"                   #  Gris

# "01" pour quoi ? (bold ?)
CL_DARKGRAY="\033[01;30m"               #  Gris foncé
CL_LIGHTRED="\033[01;31m"               #  Rouge clair
CL_LIGHTGREEN="\033[01;32m"             #  Vert clair
CL_YELLOW="\033[01;33m"                 #  Jaune
CL_LIGHTBLU= "\033[01;34m"              #  Bleu clair
CL_LIGHTMAGENTA="\033[01;35m"           #  Magenta clair
CL_LIGHTCYAN="\033[01;36m"              #  Cyan clair
CL_WHITE="\033[01;37m"                  #  Blanc

#-------------------------------------------------------

from multiprocessing import Process, Value, Lock
import os, time,math, random, sys
from array import array  # Attention : différent des 'Array' des Process

keep_running=Value('b',True) # Fin de la course ?
lyst_colors=[CL_WHITE, CL_RED, CL_GREEN, CL_BROWN , CL_BLUE, CL_MAGENTA, CL_CYAN, CL_GRAY, CL_DARKGRAY, CL_LIGHTRED, CL_LIGHTGREEN, \
             CL_LIGHTBLU, CL_YELLOW, CL_LIGHTMAGENTA, CL_LIGHTCYAN]

def effacer_ecran() : print(CLEARSCR,end='')
    # for n in range(0, 64, 1): print("\r\n",end='')

def erase_line_from_beg_to_curs() :
    print("\033[1K",end='')

def curseur_invisible() : print(CURSOFF,end='')
def curseur_visible() : print(CURSON,end='')

def move_to(lig, col) : # No work print("\033[%i;%if"%(lig, col)) # print(GOTOYX%(x,y))
    """
    Cette fonction permet de déplacer le curseur à la ligne lig et à la colonne col
    :param lig:
    :param col:
    :return:
    """
    print("\033[" + str(lig) + ";" + str(col) + "f",end='') #Ecrire à la ligne

def en_couleur(Coul) : print(Coul,end='')
def en_rouge() : print(CL_RED,end='')


def un_cheval(ma_ligne : int) : # ma_ligne commence à 0
    # move_to(20, 1); print("Le chaval ", chr(ord('A')+ma_ligne), " démarre ...")
    col=1

    while col < LONGEUR_COURSE and keep_running.value :
        mutex.acquire()
        move_to(ma_ligne+1,col)
        erase_line_from_beg_to_curs()
        en_couleur(lyst_colors[ma_ligne%len(lyst_colors)])
        print('('+chr(ord('A')+ma_ligne)+'>')
        mutex.release()

        col+=1
        mutex.acquire()
        positions[ma_ligne][1].value = col
        mutex.release()
        time.sleep(0.1 * random.randint(1,8))

def arbitre():
    """
    Le processus arbitre récupère à chaque
    :return:
    """
    while keep_running.value:



        maxi = 0
        low = 0

        for position in positions.values():
            if position[1].value > maxi:

                mutex.acquire()

                maxi = position[1].value
                move_to(22, 1)
                erase_line_from_beg_to_curs()
                en_couleur(CL_WHITE)
                print(f"Cheval ({chr(ord('A') + position[0])}> premier / position : {position[1].value}")

                mutex.release()

            if position[1].value < low:
                mutex.acquire()
                low = position[1].value
                mutex.release()
            if position[1].value == LONGEUR_COURSE:
                keep_running.value = False



#------------------------------------------------

if __name__ == "__main__" :
    mutex = Lock()
    Nb_process=20
    mes_process = [0 for i in range(Nb_process)]
    positions = {} #Ditionnaire de la forme nombre_ligne : [nombre_ligne, distance]

    LONGEUR_COURSE = 50
    effacer_ecran()
    curseur_invisible()

    for i in range(Nb_process):  # Lancer     Nb_process  processus

        positions[i] = [i, Value('i', 0)]

        mes_process[i] = Process(target=un_cheval, args=(i,))
        mes_process[i].start()


    un_arbitre = Process(target=arbitre)
    un_arbitre.start()

    move_to(Nb_process+10, 1)
    print("tous lancés")



    for i in range(Nb_process): mes_process[i].join()

    move_to(24, 1)
    curseur_visible()
    print("Fini")

