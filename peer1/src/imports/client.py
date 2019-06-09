import socket
import os
import datetime
import time
import sys

RSHost = '172.16.238.10'
RSPort = 65423
port = 10000
hostname = socket.gethostbyname(socket.gethostname())
filename = '/tmp/cookieFile.txt'


def RSrequest(message, rshost, rsport, hostname, port, cookie):
    '''
    Request builder for pier communication to RS server
    '''
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((rshost, rsport))
        trans_string = '{}\nHOST {}\nPORT {}\nCOOKIE {}\n'.format(message, hostname, port, str(cookie))
        print('Transmitting:\n{}'.format(trans_string))
        sock.sendall(trans_string.encode())
        response = sock.recv(1024).decode()
        print('Received:\n{}'.format(response))
        return response


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


def commitCookie(response):
    '''
    Client connection to register the RFC with the RS server
    '''
    cookie = openCookie(filename)
    if cookie is not 'None':
        return
    else:
        getCookie = response.split()
        file = open(filename, 'w')
        file.write(getCookie[4])
        file.close()


def RFCINDEX(queryResponse, hostname, port):
    '''
    This function is used to process output from PQUERY and retreive the index from all listening piers
    '''
    parsed = queryResponse.split()
    if len(parsed) >= 7:
        i = 7
        pier_list = []
        while i < len(parsed):
            pier_list.append(parsed[i].split('-'))
            i += 1
        for pier in pier_list:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((pier[0], int(pier[1])))
                trans_string = 'RFCINDEX\nHOST {}\nPORT {}\n'.format(hostname, port)
                sock.sendall(trans_string.encode())
                data = sock.recv(8192).decode()
                print('Forwarding:')
                print(data)
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sockpier:
                    sockpier.connect((hostname, int(port)))
                    sockpier.sendall(data.encode())
                    sockpier.close()
                sock.close()
        return pier_list

if len(sys.argv) <= 1:
    while True:
        client_in = input(
            'Please provide client action.\nAvailible actions are as follows:'
            '\nREGISTER\nLEAVE\nPQUERY\nRFCINDEX\nSEEKRFCS\n\nType QUIT and hit enter to exit... '
        )
        if client_in.upper() == 'QUIT':
            break
        elif client_in.upper() == 'REGISTER':
            register_response = RSrequest('REGISTER', RSHost, RSPort, hostname, port, openCookie(filename))
            commitCookie(register_response)
        elif client_in.upper() == 'LEAVE':
            leave_response = RSrequest('LEAVE', RSHost, RSPort, hostname, port, openCookie(filename))
        elif client_in.upper() == 'PQUERY':
            pquery_response = RSrequest('PQUERY', RSHost, RSPort, hostname, port, openCookie(filename))
        elif client_in.upper() == 'RFCINDEX':
            rfcindex_response = RFCINDEX(RSrequest('PQUERY', RSHost, RSPort, hostname, port, openCookie(filename)), hostname, port)
        elif client_in.upper() == 'SEEKRFCS':
            getrfcs_response = RSrequest('SEEKRFCS', hostname, port, hostname, port, openCookie(filename))
        else:
            print('Invalid command, please try again...\n')

else:
    if sys.argv[1].upper() == 'REGISTER':
        register_response = RSrequest('REGISTER', RSHost, RSPort, hostname, port, openCookie(filename))
        commitCookie(register_response)
    elif sys.argv[1].upper() == 'LEAVE':
        leave_response = RSrequest('LEAVE', RSHost, RSPort, hostname, port, openCookie(filename))
    elif sys.argv[1].upper() == 'PQUERY':
        pquery_response = RSrequest('PQUERY', RSHost, RSPort, hostname, port, openCookie(filename))
    elif sys.argv[1].upper() == 'RFCINDEX':
        rfcindex_response = RFCINDEX(RSrequest('PQUERY', RSHost, RSPort, hostname, port, openCookie(filename)), hostname, port)
    elif sys.argv[1].upper() == 'SEEKRFCS':
        getrfcs_response = RSrequest('SEEKRFCS', hostname, port, hostname, port, openCookie(filename))
    else:
        print('Invalid command, please try again...\n')