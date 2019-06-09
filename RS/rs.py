import socket
import threading
import socketserver
import datetime
from imports.linked import Node, LinkedList
from imports.agent import agent


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        '''
        Function responsible for handling the incoming client requests
        '''
        data = self.request.recv(1024).decode()
        parsed = data.split()
        print(data)

        #This block handles the clients REGISTER request.-----------------------
        hostname = parsed[2]
        port = parsed[4]
        cookie = parsed[-1]

        if parsed[0] == 'REGISTER':
            if cookie == 'None':
                linkedRFCServers.addPierEnd(hostname, port, linkedRFCServers.curr_cookie)
                trans_string = 'REGISTER {} OK\nCOOKIE {}\nTTL {}\nREG-NUM {}\n'.format(hostname, linkedRFCServers.curr_cookie, str(7200), str(1))
                self.request.sendall(trans_string.encode())
                linkedRFCServers.curr_cookie += 1
            
            else:
                reRegInfo = linkedRFCServers.reRegisterRFC(int(cookie))
                trans_string = 'REGISTER {} OK\nCOOKIE {}\nTTL {}\nREG-NUM {}\n'.format(
                    hostname, str(cookie),
                    str((reRegInfo[0]-datetime.datetime.now()).total_seconds()), reRegInfo[1]
                )
                self.request.sendall(trans_string.encode())

        #-----------------------------------------------------------------------


        #This block will handle the clients LEAVE request.----------------------

        elif parsed[0] == 'LEAVE':
            # If the server has no cookie they cannot leave because they have
            # not registered
            if cookie == 'None':
                trans_string = 'LEAVE FAILED\nHOST {}\nPORT {}\nHOST is not registered, invoke REGISTER to register host.'.format( parsed[3], parsed[5])
                self.request.sendall(trans_string.encode())
            # If a cookie exists, set the status and TTL of the exiting server
            else:
                leaveInfo = linkedRFCServers.leaveRFC(int(cookie))
                trans_string = 'LEAVE OK\nHOST {}\nPORT {}\nTTL {}\nSTATUS {}\n'.format(hostname, port, leaveInfo[0], leaveInfo[1])
                self.request.sendall(trans_string.encode())

        #-----------------------------------------------------------------------


        # This block will handle the clients PQUERY request.--------------------

        elif parsed[0] == 'PQUERY':
            if cookie == 'None':
                trans_string = 'PQUERY FAILED\nHOST {}\nPORT {}\nHOST is not registered, invoke REGISTER to query RS.'.format(hostname, port)
                self.request.sendall(trans_string.encode())
            else:
                piers = linkedRFCServers.pqueryRFC(int(cookie))
                if piers is not None:
                    trans_string = 'PQUERY OK\nHOST {}\nPORT {}\nPEERS:'.format(hostname, port)
                    for pier in piers:
                        trans_string += pier
                    trans_string += '\n'
                else:
                    trans_string = 'PQUERY OK\nHOST {}\nPORT {}\nPEERS\n{}'.format(hostname, port, 'No-piers-active')

                self.request.sendall(trans_string.encode())

        #-----------------------------------------------------------------------


        # This block will handle the clients KEEPALIVE request.-----------------

        elif parsed[0] == 'KEEPALIVE':
            if cookie == 'None':
                trans_string = 'KEEPALIVE FAILED\nHOST {}\nPORT {}\nHOST is not registered, invoke REGISTER to query RS.'.format(hostname, port)
                self.request.sendall(trans_string.encode())
            else:
                ttl = linkedRFCServers.keepAlive(int(cookie))
                if ttl == 0:
                    trans_string = 'KEEPALIVE FAILED\nHOST {}\nPORT {}\nHOST registration expired, invoke REGISTER to register host.'.format(hostname, port)
                else:
                    trans_string = 'KEEPALIVE OK\nCOOKIE {}\nTTL {}\nHOST is active.'.format(str(cookie), str(ttl))
                self.request.sendall(trans_string.encode())

        #-----------------------------------------------------------------------


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    '''
    Class to create the threaded TCP server.
    '''
    pass


if __name__ == "__main__":
    HOST, PORT = socket.gethostbyname(socket.gethostname()), 65423
    linkedRFCServers = LinkedList()
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address
    # start a thread with the server.
    # the thread will then start one more thread for each request.
    server_thread = threading.Thread(target=server.serve_forever)
    agent_thread = threading.Thread(target=agent, args=(linkedRFCServers,))
    agent_thread.start()
    server_thread.daemon = False
    server_thread.start()
