def send_all(sck,data):

    #t=str(type(data))

    #if t!="<class 'bytes'>":

        #raise Exception("bytes data type required")

    data_size=len(data)

    sck.send(str.encode(str(data_size)))

    sck.recv(1024)

    sck.sendall(data)

    sck.recv(1024)

def recv_all(sck):

    size=int(sck.recv(1024).decode())

    sck.send(b'ACK')

    buf=b''

    if(size%1024)==0:

        riter=int(size/1024)

    else:

        riter=int(size/1024)+1

    for i in range(riter):

        buf+=sck.recv(1024)

    sck.send(b'ACK')

    return buf






