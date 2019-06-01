"""
    Non privileged ports start from x>1023
    questions -> Dictionary of questions for asking
    answers -> Dictionary of answers for checking results

    Class Server
        __init__()
            @args
                - serverHost -> ip address or host name default:'127.0.0.1'
                - serverPort -> port number for server default: 12000
            @execution
                -  creates a socket
                    - @param AF_INET  : contains ipv4 address space
                    - @param SOCK_STREAM :  TCP connection based socket type
                    - @param SOCK_DGRAM : UDP connection-less based socket type
                -  uses socket
                -  binds socket : associate socket with a spesific network interface
                -  listen  : enables server to socket.accept() listens socket (45)->numbers of unaccapted connection
                -  creates threads for all connected clients

        MakeQuiz()
            @args
                - client -> spesifies the client
                - addr -> spesifies the client's address
            @execution
                - receives a username from client
                - while True:
                    - sends questions one by one
                    - receives answer from client
                    - if clients interrupt itself handles it
                    - when questions ended returns sends the result to client and terminates the client
"""

from socket import *
import threading

locker = threading.Lock()
questions = {
        0: """ 
            Question 1 : Select the true choices according to following:
                1. TCP is Transmission Control Protocol.
                2. UDP is User Datagram Protocol.
                3. DNS is Data Network Service.
                
                A-) 1   B-) 2  C-) 1,2  D-) 1,2,3 
                
            """,
        1: """
            Which one is NOT a Http Method ? 
            
            A-) GET  B-) POST  C-) SEND  D-) PUT
            
            """ ,
        2: """
            Which are the correct match for HTTP responses status codes ?
                1. 200 = OK
                2. 301 = Moved Permanently
                3. 400 = Not Found
                4. 404 = Bad Request
                5. 500 = Internal Server Error 
            
                A-) 1,3,5  B-) 1,2,5  C-) 1,2  D-) 4,5
            """,
        3: """
            Which one is not joint method for TCP and UDP protocols ? 
            
            A-) socket() B-) bind() C-) close() D-) send()
        
           """,
        4: """
            Which one is true for PURE P2P architecture ? 
            
            A-) No always-on server  
            B-) Arbitrary end systems directly communicate 
            C-) Peers are intermittenly connected and change IP address
            D-) Peers are continuously connected  
            
            """
}

answers = {
    0 : "C",
    1 : "C",
    2 : "B",
    3 : "D",
    4 : "D"
}


class Server:

    def __init__(self,serverHost ,serverPort):
        try:
            serverSocket = socket(AF_INET, SOCK_STREAM)
        except:
            print("Socket cannot be created!!!")
            exit(1)
        print("Socket is created...")
        try:
            serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        except:
            print("Socket cannot be used!!!")
            exit(1)
        print("Socket is being used...")
        try:
            serverSocket.bind((serverHost, serverPort))
        except:
            print("Binding cannot de done!!!")
            exit(1)
        print("Binding is done...")
        try:
            serverSocket.listen(45)
        except:
            print("Server cannot listen!!!")
            exit(1)
        print("The server is ready to receive")
        while True:
            connectionSocket, addr = serverSocket.accept()
            threading.Thread(target=self.makeQuiz, args=(connectionSocket, addr)).start()

    def makeQuiz(self,client,addr):
        pointsForUser = 0
        questionNum = 0
        client.sendto("Please give your username : ".encode(), addr)
        name = client.recv(1024)
        while True:
            try:
                sended = client.sendto(questions[questionNum].encode(), addr)
                message = client.recv(1024)
                answer = message.decode("utf-8")
                if answer is not "":
                    print(name, " says: ", message.decode("utf-8"), " for question : ", questionNum)
                    if answer is answers[questionNum]:
                        pointsForUser += 5
                    else:
                        pointsForUser += 0
            except:
                try:
                    client.sendto("Points from test: {}".format(pointsForUser).encode(), addr)
                    client.close()
                    break
                except:
                    print(name ," interrupted itself")
                    exit(1)
            questionNum += 1


if __name__=="__main__":
    serverPort=12000
    serverHost ='127.0.0.1'
    Server(serverHost,serverPort)
