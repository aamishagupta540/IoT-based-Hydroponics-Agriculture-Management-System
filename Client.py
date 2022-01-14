'''The client program sets up its socket differently from the way a server does.
  Instead of binding to a port and listening, it uses connect() to attach the socket directly to the remote address.'''
import socket
from time import sleep

host = '10.11.175.16'  # ip of the server
port = 12000  #port used by the server

def setupSocket():
    '''allow to the setup the server'''
    #create an ipv4 (AF_INET) socket object using the tcp protocol
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connection to the host on the port
    s.connect((host, port))
    return s

def sendReceive(s, message):
    s.send(str.encode(message))
    reply = s.recv(1024)  #read the data from the tcp server
    print("We have received a reply")
    print("Send closing message.")
    s.send(str.encode("EXIT"))
    s.close()
    reply = reply.decode('utf-8')  #decoding the string when receiving the data
    return reply

def transmit(message):
    s = setupSocket()
    sendReceive(s, message)
