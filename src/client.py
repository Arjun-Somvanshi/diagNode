import socket
from threading import Thread

HEADER_SIZE=10

def server_connect(Host,Port,data):
    global client
    client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect((Host,Port))
    rthread=Thread(target=connected,args=(data,client,True)).start()
    rthread.start()

def connected(data,client):
    try:
        length = len(data)
        message = "length"
        message+=str(length)
        message=message.encode('UTF-8')
        header=f"{len(message):<{HEADER_SIZE}}".encode('UTF-8')
        client.sendall(header + message)
        
        for block in data:
            message = "blocks"
            message+=str(len(block))
            message=message.encode('UTF-8')
            # header is nothing but the length of the block
            header=f"{len(message):<{HEADER_SIZE}}".encode('UTF-8')
            # we send the length of the block to server
            client.sendall(header + message)
            # we send the block then
            client.sendall(block)
    except Exception as e:
      print("Exception occured in sendMessage: "+str(e))


