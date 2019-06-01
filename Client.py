"""
class Client
    __init__()
        @args
            - serverName -> ip address default: 127.0.0.1
            - serverPort -> port number default: 120000
            - timer -> timer to get user input default : 10 seconds
        @execution
            - assign @args to local variables
            - tries to connect given ip and port spesified Server
            - exeption if cannot connect exits

    GetUserName()
        @execution
            - receives a message from server
            - takes input for Username
            - sends username to Server

    MakeQuiz()
        @execution
            - receives question from the server
            - if it is a result stops the execution and closes the client
            - calculates time before input
            - Gets an input in some seconds
            - Calculates the time passed for input
            - Sends message to server
            - Recursively calls itself until questions end

"""
from socket import *
import time


class Client:
    def __init__(self,serverName="127.0.0.1",serverPort=12000,timer=10):
        self.serverName = serverName
        self.serverPort = serverPort
        self.timer = timer
        try:
            self.clientSocket = socket(AF_INET, SOCK_STREAM)
            self.clientSocket.connect((self.serverName, self.serverPort))
        except:
            print("Cannot connect to Server")
            exit(1)

    def GetUsername(self):
        reqName = self.clientSocket.recv(1024)
        print(str(reqName,'utf-8'))
        name = input(" UserName : ")
        self.clientSocket.send(name.encode())

    def MakeQuiz(self):
        comingQ = self.clientSocket.recv(1024)
        print(str(comingQ, 'utf-8'))
        if "Points from test:" in comingQ.decode('utf-8'):
            self.clientSocket.close()
            exit(0)
        before = time.time()
        message = input("Give answer in " + str(self.timer) +" sec: ").upper()
        if time.time() - before > self.timer:
            print(self.timer," seconds passed you got 0 points from this question")
            message = "not possible answer given by user"
        if not message:
            message = "No message"
        self.clientSocket.send(message.encode())
        self.MakeQuiz()


if __name__ == '__main__':
    client = Client()
    client.GetUsername()
    client.MakeQuiz()


# here is an example without class
"""

from socket import *
import time

serverName="127.0.0.1"
serverPort=12000

clientSocket=socket(AF_INET,SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

reqName = clientSocket.recv(1024)
print(reqName)
name = input("Name : ")
clientSocket.send(name.encode())

while True:
    comingQ = clientSocket.recv(1024)
    print(str(comingQ,'utf-8'))
    if "Points from test:" in comingQ.decode('utf-8'):
        clientSocket.close()
        exit(0)
    before = time.time()
    message = input("Give answer in 10 sec: ").upper()
    if time.time() - before > 10:
        print("10 seconds passed you got 0 points from this question")
        message = "not possible answer given by user"
    if not message:
        message = "No message"
    clientSocket.send(message.encode())
"""

