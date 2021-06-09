import time
from random import randint
from multiprocessing import Process, Value, Lock, current_process, Pool


# ici je crée une classe, pour pouvoir manipuler/passer un seul objet
# Value et Lock sont à l'intérieur de cet objet
class Gas(object):
    def __init__(self, initval=9):
        self.available = Value('i', initval)
        self.lock = Lock()

    def enough_gas(self, need):
        with self.lock:
            if self.available.value >= need:
                return True
            return False

    def decrement(self, pid, need):
        with self.lock:
            print(f"\n{pid} à pris la clé et à besoin de {need} L de gaz")
            if self.available.value >= need:
                print(f"\tAssez de gaz restant: {self.available.value}.")
                print(f"\t{pid} utilise: {need} L de gaz.\n")
                self.available.value -= need
                return True
            else:
                print(f"\tPas assez de gaz restant: {self.available.value}.")
                print(f"\t{pid} relâche la clé\n")

    # def decrement(self, pid, need):
    #     # j'essaie de faire comme toi, çad: attendre qu'il y ait assez de gas
    #     while self.available.value < need:
    #         print(f"\tNot enough gas remainging: {self.available.value}.")
    #         print(f"\t{pid} waiting\n")
    #     else:
    #         # il y en a assez, je sers
    #         with self.lock:
    #             print(f"\n{pid} acquired the lock and needs {need} L of gas")
    #             print(f"\tEnough Gas remaining: {self.available.value}.")
    #             print(f"\t{pid} using: {need} L of gas.\n")
    #             self.available.value -= need
    #             return True

    def increment(self, pid, need):
        with self.lock:
            print(f"{pid} lâche la clé après avoir utilisé {need} L de gaz")
            self.available.value += need

    def current_value(self):
        with self.lock:
            return self.available.value


def worker(gas, need, repeat=2):
    pid = current_process().name
    for _ in range(repeat):
        served = gas.decrement(pid, need) # get resource
        time.sleep(3) # resource being used
        if served:
            gas.increment(pid, need) # give resource back


if __name__ == '__main__':
    gas = Gas()
    needs = [4, 5, 2, 3]
    procs = [Process(target=worker, args=(gas, need)) for need in needs]

    for p in procs:
        p.start()
    for p in procs:
        p.join()

    print(gas.current_value())
