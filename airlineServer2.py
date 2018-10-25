import socket
import sys
import threading
from numpy import *
import pickle

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(('127.0.0.1', 10000))

s2.bind(('127.0.0.1', 10002))

s.send(bytes('Server', 'utf-8'))
flightMatrix = s.recv(1024)
flightMatrix = pickle.loads(flightMatrix)
flightLocation = s.recv(1024)
flightLocation = pickle.loads(flightLocation)

def Main():

        print('Chart Update:')
        print(flightMatrix)
        while True:
            s2.listen(1)
            c, addr = s2.accept()
            
            t1 = threading.Thread(target = reserve, args = (c,addr))
            t1.daemon = True
            t1.start()
            
            t2 = threading.Thread(target = update, args = (s,))
            t2.daemon = True
            t2.start()

def reserve(c, a):
        global flightMatrix
        while True:
            c.send(bytes('Location Availability\n1.Pune\n2.Cochin\n3.Mumbai\n4.Chennai\n5.Kolkata\n(source number,destination number,number of seats):-', 'utf-8'))
            request = c.recv(1024)
            request = str(request, 'utf-8')
            request = request.split(',')
            c.send(bytes('Tickets available from '+flightLocation[int(request[0])]+' to '+flightLocation[int(request[1])]+' : '+str(flightMatrix[int(request[0])-1][int(request[1])-1]), 'utf-8'))
           
            if (flightMatrix[int(request[0])-1][int(request[1])-1] >= int(request[2])):
                flightMatrix[int(request[0])-1][int(request[1])-1] = flightMatrix[int(request[0])-1][int(request[1])-1] - int(request[2])
                c.send(bytes('Your tickets from '+flightLocation[int(request[0])]+' to '+flightLocation[int(request[1])]+' are booked', 'utf-8'))
                print('Chart Update:')
                print(flightMatrix)
                flightMatrix2 = pickle.dumps(flightMatrix)
                s.send(flightMatrix2)
           
            else:
                c.send(bytes('Tickets not available', 'utf-8'))
                
            c.send(bytes('Do you want to continue(y/n):', 'utf-8'))
            choice = c.recv(1024)
            choice = str(choice, 'utf-8')
            if choice == 'n':
                c.send(bytes('Thank You.', 'utf-8'))
                c.close
                break
def update(s):
    global flightMatrix
    while True:
        flightMatrix = s.recv(1024)
        flightMatrix = pickle.loads(flightMatrix)
    
                
if __name__ == '__main__':
    Main()
