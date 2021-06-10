from multiprocessing import Process, Value, Lock, Semaphore
from random import randint
from time import sleep, time
from os import getpid
import sys

mutex = Lock()
temptreshold = 5
presstreshold = 5
gopompe = Value('b', False)
gochauffage = Value('b', False)
temp = Value('i', 0)
press = Value('i', 0)


def controleur():
    while True:
        with mutex.lock():
            currenttemp = temp.value
            currentpress = press.value


        if currenttemp > temptreshold:
            gochauffage.value = False
            temp.value -= 1

            if currentpress > presstreshold:
                gopompe.value = True
                press.value -= 1

            else:
                gopompe.value = False

        elif currenttemp < temptreshold:
            gopompe.value = True
            gochauffage.value = True
        elif currenttemp == temptreshold:
            gochauffage.value = False
            if currentpress > presstreshold : gopompe.value = True
            else: gopompe.value = False

        sleep(0.5)


def chauffage():
    while True:
        if gochauffage.value:
            press.value += 1

        sleep(1)


def temperature():
    while True:

