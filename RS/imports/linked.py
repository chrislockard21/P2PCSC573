import datetime
import time

class Node():
    '''
    Creates a node in the linked list for the piers coming in and out of the system
    '''
    def __init__(self, hostname, port, cookie):
        '''
        Initializes the Node object
        '''
        self.hostname = hostname
        self.port = int(port)
        self.cookie = cookie
        self.status = 'active'
        self.TTL = datetime.datetime.now() + datetime.timedelta(0, 7200)
        self.reg_time = datetime.datetime.now()
        self.reg_num = 1
        self.next = None

    def __repr__(self):
        '''
        Visual representation of Node when printed
        '''
        return 'PEER\nHOST {}\nPORT {}\nTTL {}\nSTATUS {}'.format(
                    self.hostname, str(self.port), self.TTL, self.status
                )
                

class LinkedList():
    '''
    LinkedList class creates a linked list and establishes methods to append
    the list walk its contents, and return data for queries
    '''
    def __init__(self):
        '''
        Initializes the linked list
        '''
        self.startNode = None
        self.curr_cookie = 1

    def reRegisterRFC(self, cookie):
        '''
        Controls the re-registation of nodes
        '''
        if self.startNode is None:
            print('No RFCs to list')
            return
        else:
            n = self.startNode
            while n is not None:
                if cookie == n.cookie:
                    n.status = 'active'
                    n.TTL = datetime.datetime.now() + datetime.timedelta(0, 7200)
                    n.reg_num += 1
                    n.reg_time = datetime.datetime.now()
                    return (n.TTL, n.reg_num)
                n = n.next

    def leaveRFC(self, cookie):
        '''
        Controls the leave request from piers
        '''
        if self.startNode is None:
            print('No RFCs to list')
            return
        else:
            n = self.startNode
            while n is not None:
                if cookie == n.cookie:
                    n.status = 'inactive'
                    n.TTL = 0
                    return (n.TTL, n.status)
                n = n.next

    def addPierEnd(self, hostname, port, cookie):
        '''
        Adds a RFC pier to the end of the linked list
        '''
        newNode = Node(hostname, port, cookie)
        if self.startNode is None:
            self.startNode = newNode
            return
        n = self.startNode
        while n.next is not None:
            n = n.next
        n.next = newNode

    def pqueryRFC(self, cookie):
        '''
        Function that returns the pier list for a PQUERY
        '''
        if self.startNode is None:
            return None
        else:
            n = self.startNode
            pier_list = []
            while n is not None:
                if n.status == 'active' and cookie != n.cookie:
                    pier_list.append('\n{}-{}'.format(n.hostname, n.port))
                n = n.next
            return pier_list
        
    def keepAlive(self, cookie):
        '''
        Function that resets the TTL to keep the peer alive
        '''
        if self.startNode is None:
            print('No peers to keep alive')
            return
        else:
            n = self.startNode
            while n is not None:
                if cookie == n.cookie:
                    if  n.status == 'inactive':
                        return 0
                    else:
                        n.TTL = datetime.datetime.now() + datetime.timedelta(0, 7200)
                        return (n.TTL - datetime.datetime.now()).total_seconds()
                n = n.next