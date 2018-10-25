import socket
import threading
import numpy as np
import pickle 

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#matrix of ticket availability
flightMatrix = np.array([[0,12,9,3,0],
                      [10,0,20,7,4],
                      [9,11,0,5,3],
                      [30,2,15,0,8],
                      [0,8,13,20,0]])
flightMatrix = np.reshape(flightMatrix,(5,5))

flightLocation = {1:'Pune',
                  2:'Cochin',
                  3:'Mumbai',
                  4:'Chennai',
                  5:'Kolkata'}

#available server list for clients to connect to
servers = [10001,10002,10003]

connections = []

s.bind(('127.0.0.1', 10000))

def Main():
        while True:
            print("Main Server Running")
            s.listen(1)
            c, addr = s.accept()
            typeofConn = c.recv(1024)
            
            if not typeofConn:
                break;
                
            #check to find whther incoming connection is a client or a server
            if str(typeofConn,'utf-8') == 'Client':
                c.send(bytes('Welcome to LightSpeed Airlines', 'utf-8'))
                server2 = pickle.dumps(servers)
                c.send(server2)

            if str(typeofConn,'utf-8') == 'Server':
                connections.append(c)
                flightMatrix2 = pickle.dumps(flightMatrix)
                c.send(flightMatrix2)
                flightLocation2 = pickle.dumps(flightLocation)
                c.send(flightLocation2)
                
                #thread for continous update of flightmatrix from various servers
                t1 = threading.Thread(target = update, args = (c,addr))
                t1.daemon = True
                t1.start()
                
        print("Main Server Stopped")
                
def update(c,addr):
    global flightMatrix
    while True:
        data = c.recv(1024)
        
        if not data:
            break;
            
        flightMatrix = pickle.loads(data)
        #send update to all servers
        for connection in connections:
            flightMatrix2 = pickle.dumps(flightMatrix)
            connection.send(flightMatrix2)
            

            
if __name__ == '__main__':
    Main()