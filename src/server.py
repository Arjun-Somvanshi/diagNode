from contextlib import nullcontext
from threading import Thread
import socket
import pickle


HEADER_SIZE=10


check=True

listLength = None
List = []

def changeCheck(c):
    global check
    check = c

def accept():
    global server_socket
    client_socket,client_addr = server_socket.accept()        #threads are just created for making blocks of code execute parallely! like accepting the connections and handling clients all these work in parallel
    print("A client has been connected to the server!")
    connected(client_socket)

def connected(client):
    global List, listLength
    try:
        length=client.recv(HEADER_SIZE).decode('UTF-8')
        message=client.recv(int(length)).decode('UTF-8')

        listLength = int(message[6:])
        print(listLength)
        for x in range(listLength):
            length=client.recv(HEADER_SIZE).decode('UTF-8')
            message=client.recv(int(length)).decode('UTF-8')
            print(message)
            List.append(client.recv(int(message[6:])))
        for x in List:
            print(x)
            print("-------------------------")

    except Exception as e:
        print("exception in connected: "+str(e)) 
        client.close()

def clearList():
    global listLength,List
    listLength = None
    List = []

def getListLength():
    global listLength,List
    return listLength

def getList():
    global List
    return List

"""
    1) startListening -- listens for the client
    2) make a while loop and just iterate it until ListLength is not None
    3) make a while len(getList())!=getListLength():
            edit the shared variable of the progress bar
    4) clearList()
  
"""


server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
def startListening(port):
    global server_socket
    Host=""
    server_socket.bind((Host,port))
    server_socket.listen(50)
    print("Server is listening for clients!!")
    main_thread=Thread(target=accept)
    main_thread.start() #starts the thread
    main_thread.join() #blocks the code here till the main_threads execution doesn't end!
    server_socket.close()

if __name__=="__main__":
    startListening(8000)
