import pickle
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15
from Crypto.PublicKey import RSA
from security import blake
class Block():
    def __init__(self):
        self.date = self.get_time()
        self.medical_data = {"doctorName": '', 'height': 0, "age": 0, 
                        "weight": 0, "bloodgroup": '', "symptoms": [],
                        "tests": {}, "treatments":{}, "bill": {}
                        } 
        self.user_hash = None
        self.prev_block_hash = None
        self.block_hash = None
        self.signature = None
        self.signer_hash = None # This is the super nodes identity

    def get_time(self): 
        from datetime import datetime
        time_now = datetime.now()
        return time_now.strftime("%B %d, %Y@%H:%M:%S")

class BlockChain():
    def __init__(self, userHash):
        # collection of the blocks
        self.chain = []
        self.genensisBlock = Block()
        self.genensisBlock.user_hash = userHash
        hashObj, self.current_block_hash = self.hashBlock(self.genensisBlock)
        self.genensisBlock.block_hash = self.current_block_hash
        self.chain.append(self.genensisBlock)

    def appendBlock(self, medicalData, userHash, signerPrivateKey, signer_hash):
        block = Block()
        block.medical_data = medicalData
        block.user_hash = userHash
        block.signer_hash = signer_hash
        block.prev_block_hash = self.current_block_hash
        hashObj, block.block_hash = self.hashBlock(block)
        block.signature = pkcs1_15.new(signerPrivateKey).sign(hashObj)
        self.current_block_hash = block.block_hash
        self.chain.append(block)

    def verifyBlock(self, block, signerPublicKey):
        hashObj, blockHash = self.hashBlock(block)
        try:
            pkcs1_15.new(signerPublicKey).verify(hashObj, block.signature)
            print("Block Verified.")
        except:
            print("Verification Failed")
    
    def hashBlock(self, block):
        blockCopy = Block()
        blockCopy.date = block.date
        blockCopy.user_hash = block.user_hash
        blockCopy.signer_hash = block.user_hash
        blockCopy.medical_data = block.medical_data
        blockAsBytes = pickle.dumps(blockCopy)
        blockHash = SHA256.new(blockAsBytes)
        return blockHash, blockHash.hexdigest()
    
    def showBlockChainCli(self):
        a = 0
        for block in self.chain:
            if a != 0:
                print("              /\\")
                print("             /  \\")
                print("              ||")
                print("              ||")
            else:
                a+=1
            print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            print("            START BLOCK")
            print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            print("Date: ", block.date)
            print("Block Hash: ", block.block_hash)
            print("Medical Data: ", block.medical_data)
            print()
            print("Previous Block Hash: ", block.prev_block_hash)
            print()
            print("User hash: \n", block.user_hash)
            print()
            print("Hospital Signature: \n", block.signature)
            print()
            print("Hospital Identification Hash \n", block.signer_hash)
            print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            print("           END BLOCK")
            print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")


if __name__ == "__main__":
    username_hash = blake("Arjun")                
    password_hash = blake("arjun1922")                

    hospital_admin_username = blake("Raahil")
    hospital_admin_password = blake("raahil2022")

    credentials = username_hash + password_hash
    credentialsHospital = hospital_admin_username + hospital_admin_password 
    
    signer_private_key = RSA.generate(2048)
    signer_public_key = signer_private_key.publickey()

    if(False):
        print("Writing blockchain to memory")
        medical_data = {"sick": "yes I have headache"}
        blockChain = BlockChain(credentials)
        blockChain.appendBlock(medical_data, credentials, signer_private_key, credentialsHospital)

        medical_data = {"sick": "stomach ache bro"}
        blockChain.appendBlock(medical_data, credentials, signer_private_key, credentialsHospital)

        blockChain.showBlockChainCli()
        print()

        with open("../UserData/blockchain.bin", 'wb') as f:
            pickle.dump(blockChain, f, pickle.HIGHEST_PROTOCOL) 

    else:
        print("Loading the blockchain from memory")
        with open("../UserData/blockchain.bin", 'rb') as f:
            blockChain = pickle.load(f) 
        medical_data = {"sick": "sick of hippie black metal that sounds like djent is having a baby"}
        blockChain.appendBlock(medical_data, credentials, signer_private_key, credentialsHospital)
        blockChain.showBlockChainCli()














