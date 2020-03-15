import socket
from threading import Thread

#this code is to be used in a helper function in main/routes 

"""
 This class is used to easily set up and manage multiple sockets in the webapp 
 
"""
class Socket(object):

    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.send_buffer 
        self.recv_buffer

        #open socket connection
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    """
    Recieves data from the other subsystems
    Returns the status code from the subsytem
    """
    def recv(self):
        self.s.bind((self.host, self.port))
        self.listen()

        conn, addr = self.s.accept()

        waiting = True

        with conn:
            print('Connected by', addr)
            while waiting:
                #this line hangs until it recieves the data 
                data = conn.recv(1024)
                if not data:
                    break
                self.recv_buffer = data 
                waiting = False
        
        return self.recv_buffer

    """
    Sends data through the socket
    Returns True if the data is send correctly, false otherwise
    """
    def send(self, msg):
        self.s.connect((self.host, self.port))
        self.send_buffer = msg
        try:  
            self.s.sendall(msg.encode('UTF-8'))
        except socket.error:
            print("Error sending data:")
            return False

        return True

                            

    