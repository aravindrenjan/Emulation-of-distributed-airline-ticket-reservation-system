import socket
import threading
import pickle

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 10000))


def Main():
        while True:
            s.send(bytes('Client', 'utf-8'))
            data = s.recv(1024)
            print(str(data,'utf-8'))
            data = s.recv(1024)
            servers = pickle.loads(data)
            
            #connection 'try's to various servers
            try:
                s2.connect(('127.0.0.1',servers[0]))
            except:
                try:
                    s2.connect(('127.0.0.1',servers[1]))
                except:
                    try:
                        s2.connect(('127.0.0.1',servers[2]))
                    except:
                        print("All servers are down")
            finally:    
                t2 = threading.Thread(target = sendMsg)
                t2.daemon = True
                t2.start()
        
                while True:
                    data = s2.recv(1024)
                    if not data:
                        break
                    print(str(data, 'utf-8'))
        

def sendMsg():
        while True:
            s2.send(bytes(input(''), 'utf-8'))
            
            
if __name__ == '__main__':
    Main()
