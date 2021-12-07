import socket
from threading import Thread
from blockchain import *

HEADER_SIZE=10

def server_connect(Host,Port,data):
    global client
    client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect((Host,Port))
    Thread(target=connected,args=(data,client)).start()

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

if __name__ == "__main__":
    username_hash = blake("Arjun")                
    password_hash = blake("arjun1922")                

    hospital_admin_username = blake("Raahil")
    hospital_admin_password = blake("raahil2022")

    credentials = username_hash + password_hash
    credentialsHospital = hospital_admin_username + hospital_admin_password 
    
    signer_private_key = RSA.generate(2048)
    signer_public_key = signer_private_key.publickey()
    
    medical_data = {"sick": "yes I have headache"}
    blockChain = BlockChain(credentials)
    blockChain.appendBlock(medical_data, credentials, signer_private_key, credentialsHospital)
    serializedBlockList = [pickle.dumps(blockChain.chain[1])]
    print(serializedBlockList)
    server_connect("127.0.0.1", 8000, serializedBlockList)

