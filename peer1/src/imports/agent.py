import time
import socket
import datetime
import os

def openCookie(filename):
    '''
    Opens and reads cookie files
    '''
    if not os.path.isfile(filename):
        cookie = 'None'
    else:
        file = open(filename, 'r')
        cookie = file.read()
        file.close()
    return cookie

def agent(RSHost, RSPort, HOST, PORT):
    '''
    Agent function that traverses a linked list and sets the status
    of all nodes with TTL <= 0 to inactive
    '''
    filename = '/tmp/cookieFile.txt'
    while True:
        time.sleep(1000)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((RSHost, RSPort))
            trans_string = 'KEEPALIVE\nHOST {}\nPORT {}\nCOOKIE {}\n'.format(HOST, PORT, openCookie(filename))
            sock.sendall(trans_string.encode())
            print(sock.recv(1024).decode())