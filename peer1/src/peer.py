import socket
import threading
import socketserver
import datetime
import time
from imports.linked import Node, LinkedList
import os
from imports.agent import agent


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        '''
        Function responsible for handling the incoming client requests
        '''
        # Accepts the incomming data from a client
        data = self.request.recv(8192).decode()
        parsed = data.split()

        # Grabs the hostname and port from incomming requests
        hostname = parsed[2]
        port = parsed[4]

        # Handles any requests from a clinets rfcindex request
        # This request is forwarded from the client to the peer so that the
        # index can be comitted to the peers linked list
        if parsed[0] == 'RFCINDEX' and parsed[1] == 'OK':
            if len(parsed) > 6 and parsed[-1] != 'No-List':
                # Gets a list of all active RFCs registered on this peer
                RFC_current = linkedRFCIndex.RFCsActive()
                i = 7
                while i < len(parsed):
                    RFC = parsed[i].split('|')
                    # Ensures that the same rfc is not appended to the list if it is
                    # already contained by the host and active
                    # multiple records can occur if a record is inactive
                    if RFC[0] not in RFC_current:
                        linkedRFCIndex.addRFCRecordEnd(RFC[0], RFC[1], RFC[2], RFC[3])
                    else:
                        continue
                    i += 1

        # Handles requests for the peers rfcindex
        elif parsed[0] == 'RFCINDEX':
            print(data)
            trans_string = 'RFCINDEX OK\nHOST {}\nPORT {}\nRFCs\n'.format(hostname, port)
            RFC = linkedRFCIndex.RFCIndex()
            # Appends all rfcs in the linked list to the transmission message
            for R in RFC:
                trans_string += R
            self.request.sendall(trans_string.encode())

        # Handles requests from the client to initiate the loop to download all
        # rfc files that are currently in the peers linked list
        elif parsed[0] == 'SEEKRFCS':
            RFC_staging = linkedRFCIndex.RFCIndex()
            total_time = 0
            # Loops through rfc index
            for R in RFC_staging:
                RFC = R.split('|')
                # Check that the rfc is not hosted on the current peer
                if RFC[2] != HOST:
                    trans_string = 'GETRFC\nHOST {}\nPORT {}\n{}\n'.format(HOST, PORT, RFC[0]+ ' ' +RFC[1])
                    # Opens a socket to send a getrfc request to the host/port specified in the index
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                        sock.connect((RFC[2], int(RFC[3])))
                        sock.sendall(trans_string.encode())
                        # Opens a file on the peer to accept the incoming data and write it to the peer
                        with open('/var/opt/RFCs/' + RFC[0]+RFC[1], 'w') as f:
                            print('receiving data...')
                            start = datetime.datetime.now()
                            while True:
                                # Data is received
                                data = sock.recv(1024).decode()
                                if not data:
                                    print('done receiving.')
                                    finish = (datetime.datetime.now() - start).total_seconds()
                                    print('time: ' + str(finish) + '\n')
                                    total_time += finish
                                    break
                                f.write(data)
            print('-----------------------------------------------------')
            print('Total time:',total_time)
            trans_string = 'SEEKRFCS OK\nHOST {}\nPORT {}\nTOTAL TIME {}\n'.format(HOST, PORT, total_time)
            self.request.send(trans_string.encode())
                    
        # Handles the getrfc request and begins the transfer to the peer who requested it
        elif parsed[0] == 'GETRFC':
            print(data)
            parsed = data.split()
            # Gets the filename information from the incoming request
            filename = '/var/opt/RFCs/' + parsed[-2] + parsed[-1]
            f = open(filename, 'rb')
            l = f.read(8192)
            print('sending data...')
            while (l):
                self.request.send(l)
                l = f.read(1024)
            f.close()


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    '''
    Class to create the threaded TCP server.
    '''
    pass

if __name__ == "__main__":
    # port 0 means to select an arbitrary unused port
    HOST, PORT = socket.gethostbyname(socket.gethostname()), 10000
    RSHost = '172.16.238.10'
    RSPort = 65423
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    linkedRFCIndex = LinkedList()
    RFCPath = '/var/opt/RFCs'

    RFCfiles = [f for f in os.listdir(RFCPath) if os.path.isfile(os.path.join(RFCPath, f))]
    if len(RFCfiles) > 0:
        for f in RFCfiles:
            if f[:1] != '.':
                number = f[:4]
                title = f[4:]
                linkedRFCIndex.addRFCRecordEnd(number, title, HOST, PORT)
    
    ip, port = server.server_address

    # start a thread with the server.
    # the thread will then start one more thread for each request.
    server_thread = threading.Thread(target=server.serve_forever)
    agent_thread = threading.Thread(target=agent, args=(RSHost, RSPort, HOST, PORT))
    agent_thread.start()
    # agent_thread = threading.Thread(target=agent)
    # agent_thread.start()
    # exit the server thread when the main thread terminates
    server_thread.daemon = False
    server_thread.start()
