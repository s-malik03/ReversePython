def send_all(sck,data):

    #python3 only

    #t=str(type(data))

    #if t!="<class 'bytes'>":

        #raise Exception("bytes data type required")

    data_size=len(data)

    sck.send(str.encode(str(data_size)))

    if sck.recv(1024)!=b'ACK':

        raise "SEND ERROR"

    sck.sendall(data)

    if sck.recv(1024)!=b'ACK':

        raise "SEND ERROR"

def recv_all(sck):

    size=int(sck.recv(1024).decode())

    sck.send(b'ACK')

    buf=b''

    if(size%4096)==0:

        riter=int(size/4096)

    else:

        riter=int(size/4096)+1

    for i in range(riter):

        buf+=sck.recv(4096)

    sck.send(b'ACK')

    return buf

def ftrans(sck,fname):

    try:

        fhandle=open(fname,'rb')

        data=fhandle.read()

        data_len=len(data)

        print("Sending "+str(data_len)+" bytes of data.")

        sck.send(str.encode(str(data_len)))

        print(sck.recv(1024))

        sck.send(str.encode(fname))

        print(sck.recv(1024))

        sck.sendall(data)

        print("Data sent.")

        print(sck.recv(1024))

        fhandle.close()

    except:

        print("FTRANS ERROR!")

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







