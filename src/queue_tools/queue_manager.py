#!/usr/bin/env python3
import subprocess
import sys
import time
import threading 

class myThread(threading.Thread):
    def __init__(self, threadID, data):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.data = data
    def run(self):
        while (not (self.data == ['False'])):
            #PUT ANALYSIS HERE
            subprocess.run(["./pop_line", "DAQueue", str(self.threadID)])
            self.data = qCheck(self.threadID)
        myLock.acquire()
        freeThreads.add(self.threadID)
        myLock.release()

def qCheck(t):
    p = subprocess.Popen(["./queue_check", "DAQueue", str(t)], stdout=subprocess.PIPE)
    a, err = p.communicate()
    a = a.decode("UTF-8").rstrip().split(";")
    return a    


nThreads = sys.argv[1]  
nThreads = int(nThreads)
freeThreads = set()
usedThreads = set()
myLock = threading.Lock()

for i in range(0, nThreads):
    freeThreads.add(i+1)

subprocess.run(["./init_check", "DAQueue"])

while True:
    myLock.acquire()
    if freeThreads:
        for t in freeThreads:
            data = qCheck(t)
            if (not (data == ['False'])):
                myThread(t, data).start()
                usedThreads.add(t)
        freeThreads = freeThreads - usedThreads
        usedThreads = set()
    myLock.release()
    time.sleep(15)
