# Mai 2021
# Ex Event : création/set/wait

import multiprocessing as mp
import time

def task(event, timeout):
    print("Started process but waiting for event...")
    # make the process wait for event with timeout set
    event_set = event.wait(timeout)
    if event_set:
        print("Event received, releasing process...")
    else:
        print("Time out, moving ahead without event...")

if __name__ == '__main__':
    # initializing the event object
    e = mp.Event()

    # starting the process
    process1 = mp.Process(name='Event-Blocking-process', target=task, args=(e,4))
    process1.start()
    # sleeping the main process for 3 seconds
    time.sleep(3)
    # generating the event
    e.set()
    print("Event is set.")
"""
Started process but waiting for event...
Event received, releasing process...
Event is set.
"""
