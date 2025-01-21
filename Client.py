
from  Communicator import Communicator
from socket import *
import json
import threading 
import time
class Client:
    def __init__(self,ID):
        self.Id=ID
        self.socket=socket(AF_INET,SOCK_STREAM) 
        self.comm=Communicator()
        self.Status="Online"
    def connectToServer(self,Port):
        try:
            self.socket.connect(Port)
            print(f"Connection sucesful on Server With Port Number{Port}")
        except:
            raise error("faileds")
    
    def SendMessage(self,msg):
        self.comm.SendMessage(self.socket,msg)

    def RecieveMsg(self):
       return self.comm.ReceiveMsg(self.socket)
   
    
    def SendStatus(self,urgent=None):
        JsonData={
            "id":self.Id,
            "status":self.Status
        };
        if urgent:
           JsonData["id"]=urgent;
           self.SendMessage(json.dumps(JsonData))
           return;
        while self.Status=="Online":
            try:
                self.SendMessage(json.dumps(JsonData))
                time.sleep(5)
            except OSError:
                print("Server disconnected")

    def listenMessages(self):
        while self.Status=="Online":
            msg=self.comm.ReceiveMsg(self.socket)
            print(f"Message Received from Server: {msg}");
            if "command" in msg:
                print("Turning off the client")
                resp=json.loads(msg)
                if resp['command']=='poweroff':
                    self.SendStatus(urgent="Offline")
                    self.Status=='Offline'



    
    def Run(self): 
                # Create threads  
        StatusThread = threading.Thread(target=self.SendStatus, args=())  
        ListeningThread = threading.Thread(target=self.listenMessages, args=())  
        
        # Start the threads  
        StatusThread.start()  
        ListeningThread.start()  
        
        # Optionally wait for threads to finish  
        
        StatusThread.join()  
        ListeningThread.join()  
       

C=Client(input("Enter ID"))
C.connectToServer(("localhost",4200))
C.Run()