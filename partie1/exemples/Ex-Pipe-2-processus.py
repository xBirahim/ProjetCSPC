from multiprocessing import Process, Pipe

def worker(num, cote_fils):
    if num==1 :
        cote_fils.send([42,"is","the", "best"])
    else:
        cote_fils.send('Hello')
    cote_fils.close()

if __name__ == '__main__':
    cote_pere, cote_fils= Pipe()
    p1 = Process(target=worker, args=(1, cote_fils))
    p1.start()
    p2 = Process(target=worker, args=(2, cote_fils))
    p2.start()
    print(cote_pere.recv())  
    print(cote_pere.recv()) 
    p1.join()
    p2.join()
"""
[42, 'is','the', 'best']
Hello
"""
