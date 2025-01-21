from socket import *  

class Communicator:  
    def __init__(self):  
        pass  

    def SendMessage(self, socket, Msg):  
        socket.send(Msg.encode())  

    def ReceiveMsg(self, socket):  
        data = socket.recv(2048).decode()  
        return data