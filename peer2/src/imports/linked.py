import socket
import threading
import socketserver
import datetime
import time

class Node():
    '''
    Class that creates a new node for an RFC with the payload information.
    '''
    def __init__(self, RFCNum, RFCTitle, hostname, port):
        self.RFCNumb = RFCNum
        self.RFCTitle = RFCTitle
        self.hostname = hostname
        self.port = port
        self.TTL = datetime.datetime.now() + datetime.timedelta(0, 7200)
        self.next = None

class LinkedList():
    '''
    Class that contains the payloads of the RFC servers. The class is
    initialized at the start of this script which starts the RS server.
    '''
    def __init__(self):
        self.startNode = None

    def addRFCRecordEnd(self, RFCNumb, RFCTitle, hostname, port):
        '''
        Adds an RFC reccord to the linked list
        '''
        newNode = Node(RFCNumb, RFCTitle, hostname, port)
        if self.startNode is None:
            self.startNode = newNode
            return
        n = self.startNode
        while n.next is not None:
            n = n.next
        n.next = newNode

    def RFCIndex(self):
        if self.startNode is None:
            RFCList = 'No-List'
            return RFCList
        else:
            n = self.startNode
            RFCList = []
            while n is not None:
                RFCList.append('{}|{}|{}|{}\n'.format(n.RFCNumb, n.RFCTitle, n.hostname, n.port))
                n = n.next
            return RFCList

    def walkList(self):
        if self.startNode is None:
            print('No RFCs to show')
            return
        else:
            n = self.startNode
            while n is not None:
                print(n.RFCNumb, n.RFCTitle)
                n = n.next

    def RFCsActive(self):
        if self.startNode is None:
            RFCList = 'No-List'
            return RFCList
        else:
            n = self.startNode
            RFCList = []
            while n is not None:
                if (n.TTL - datetime.datetime.now()).total_seconds() > 0:
                    RFCList.append(n.RFCNumb)
                n = n.next
            return RFCList