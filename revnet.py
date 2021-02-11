import socket
class ClientConn():

    def __init__(self,Host,Port):

        self.Socket=socket.socket()

        try:

            self.Socket.connect((socket.gethostbyname(Host),Port))

        except:

            print("Connection Failed.")

    def sendstring(self,Str):

        self.Socket.sendall(Str.encode('utf-8'))

        self.Socket.send('^&*!stop(())'.encode('utf-8'))

    def sendfile(self,FileName):

        try:

            FileHandler=open(FileName,'rb')

            while True:

                Data=FileHandler.read(1024)

                if not Data:

                    break

                self.Socket.sendall(Data)

            self.Socket.sendall(b'^&*!stop(())')
            FileHandler.close()
            return "Successful"

        except:

            return "Unable to open file "+FileName

    def recvfile(self,FileName):

        FileHandler=open(FileName,'wb')

        while True:

            Data=self.Socket.recv(1024)

            if b'^&*!stop(())' in Data:

                break

            FileHandler.write(Data)

        FileHandler.close()

    def recvstring(self):

        Str=''

        while True:

            Data=self.Socket.recv(1024)

            if b'^&*!stop(())' in Data:

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
