import socket
class ClientConn():

    def __init__(self,Host,Port):

        self.Socket=socket.socket()

        try:

            self.Socket.connect((socket.gethostbyname(Host),Port))

        except:

            print("Connection Failed.")

    def sendstring(self,Str):

        for S in Str:

            self.Socket.send(S.encode('utf-8'))
            
        self.Socket.send('^&*!stop(())'.encode('utf-8'))

    def sendfile(self,FileName):

        try:

            FileHandler=open(FileName,'rb')

            while True:

                Data=FileHandler.read(1024)

                if not Data:

                    break

                self.Socket.send(Data)

            self.Socket.send(b'^&*!stop(())')
            FileHandler.close()
            return "Successful"

        except:

            return "Unable to open file "+FileName

    def recvfile(self,FileName):

        FileHandler=open(FileName,'wb')

        while True:

            Data=self.Socket.recv(1024)

            if Data==b'^&*!stop(())':

                break

            FileHandler.write(Data)

        FileHandler.close()

    def recvstring(self):

        Str=''

        while True:

            Data=self.Socket.recv(1024)

            if Data==b'^&*!stop(())':

                break

            Str=Str+Data.decode('utf-8')

        return Str

    def close(self):

        self.Socket.close()

class ServerConn(ClientConn):

    def __init__(self, Host, Port):

        self.SocketServer=socket.socket()
        self.SocketServer.bind((Host,Port))
        self.SocketServer.listen()
        self.Socket,self.SocketAddr=self.SocketServer.accept()