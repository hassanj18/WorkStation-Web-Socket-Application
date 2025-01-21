from socket import *
from Communicator import *
import time
from json import *
import threading

class Workstation:
    def __init__(self,id,Status,sok):
        self.ID=id;
        self.status=Status
        self.socket=sok
    def __str__(self):
        return f"ID={self.ID} Status={self.status}"
    def GetStatus(self):
        return self.status
    def GetID(self):
        return self.ID
    def GetSok(self):
        return self.socket
    def UpdateStatus(self,id,st):
        self.ID=id;
        self.status=st;


class Server:
    def __init__(self):
        self.socket=socket(AF_INET,SOCK_STREAM) 
        self.comm=Communicator()
        self.Workstations=dict()
    def StartListening(self,Port):
        try:
            self.socket.bind(Port)
            self.socket.listen(5)
            print("Server Started Listening Succesfully")
        except:
            raise error("Server Starting Error")
    
    def SendMessage(self,msg,clientSok):
        self.comm.SendMessage(clientSok,msg)

    def RecieveMsg(self,clientSok):
       return self.comm.ReceiveMsg(clientSok)
   
    def SendBroadcast(self,msg):
        for addrs in self.Workstations:
            self.comm.SendMessage(self.Workstations[addrs].GetSok(),msg)
    
    def SendMsgtoWorkStation(self,ID,msg):
        for addrs in self.Workstations:
            if self.Workstations[addrs].GetID()==ID:
                if self.Workstations[addrs].GetStatus()=="Online":
                    self.comm.SendMessage(self.Workstations[addrs].GetSok(),msg)
                    print("message Sent")
                    return;
        print("Invalid ID")

    def Input(self):
        while True:
            choice=str(input("Select Available Methods:\n Broadcast.\n Individual"))
            if choice.lower()=='broadcast':
                cmd=str(input("Please Choose Command \n1)PowerOff."));
                if cmd.lower()=="poweroff":
                    msg={
                        "command":"poweroff"
                    }
                    self.SendBroadcast(dumps(msg));
            elif choice.lower()=='individual':
                cmd=str(input("Please Choose Command \n1)PowerOff."));
                for i in self.Workstations:
                    print(self.Workstations[i])
                id=str(input("Please enter ID"))
                if cmd.lower()=="poweroff":
                    msg={
                        "command":"poweroff"
                    }
                    self.SendMsgtoWorkStation(id,dumps(msg))
            else:
                print("Invalid Cmd")

    def ReceiveStatus(self,clientsok,addrs):    
        while True:
            jsonStr=self.comm.ReceiveMsg(clientsok)
            # self.SendMessage("Acked",clientsok)
            if not jsonStr:
                print(f"client{addrs} disconnected");
                del self.Workstations[addrs];
            Status=loads(jsonStr)
            # print(f"Workstation Sent status{Status}")
            self.Workstations[addrs].UpdateStatus(Status["id"],Status["status"])
            
            while Status["status"]=="Offline":
                pass
                    
           
    
    def Run(self):
        #inputth=threading.Thread(target=self.Input,args=())
        #inputth.start()
        while True:        
                c,addrs=self.socket.accept()
                if c not in self.Workstations:
                    self.Workstations[f"{addrs}"]=Workstation(None,"Online",c)
                    print("Workstation Added");
                    Th = threading.Thread(target=self.ReceiveStatus, args=(c,str(addrs)))
                    Th.start()
                    
