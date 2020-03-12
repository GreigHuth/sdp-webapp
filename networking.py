import socket
from threading import Thread
    

class x_socket(object):

    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.send_buffer 
        self.recv_buffer

        self.running = False


    """
    Starts thread socket so it can recieve and send packets
    """
    def start(self):

        self.running =  True 
        Thread(target=self.update, args=()).start()

    def update(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            conn, addr = s.accept()
        with conn:
            while self.running:
                self.recv = conn.recv(1024)
                if not self.recv:
                    break
                            

