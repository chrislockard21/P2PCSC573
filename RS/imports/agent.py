import time
import datetime

def agent(LinkedList):
    '''
    Agent function that traverses a linked list and sets the status
    of all nodes with TTL <= 0 to inactive
    '''
    while True:
        time.sleep(2)
        if LinkedList.startNode is None:
            return
        else:
            n = LinkedList.startNode
            while n is not None:
                TTL = (n.TTL - datetime.datetime.now()).total_seconds()
                if TTL <= 0:
                    n.status = 'inactive'
                n = n.next