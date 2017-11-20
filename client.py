import socket
import time
import sys

class Client:
    __init__(self,cashAvailable):
        self.ballance = cashAvailable
        self.yielding = None
        self.purchasedStocks  = []
        self.favoriteStocks   = []
    
class Stack:
    def __init__(self):
        self.list = []
    def push(self,item):
        self.list.append(item)
    def pop(self):
        return self.list.pop()
    def isEmpty(self):
        return len(self.list) == 0

#server should get the first string in each array of strings
def startTransaction(action,client,numStocks,price,serverIP="192.168.1.11",portNum=2044):
    try:
        clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    except socket.error,msg:
        print "failed. error code: "+ str(msg[0])+ " and error msg = "+msg[1]
        sys.exit()
        
    if action == "BUY":
        #stock randomly selected from list of favorite stocks 
        stock = None
    elif action == "SELL":
        #stock randomly selected from purchased
        stock = None
    else:
        pass
    
    clientSocket.connect((serverIP,portNum))
    clientSocket.sendall(action+" "+stock+" "+numStocks+" "+price)    
    
    #should receive message saying  buy/sell success 
    recvMsg = clientSocket.recv(4096) 
    
    
    #Update with correct format
    print "recieved message = ",recvMsg
    if(recvMsg == "SUCCESS"):
        #update stocks
        time.sleep(1)   #time in seconds
        
    
    clientSocket.close()


#function to get info from text file and push to a stack
def getInfo(textFile,stockStack):
    with open(textFile,"r") as file:
            for line in file:
                x = line
                #String formatting done here
                stockStack.push(x)
    
if __name__ == "__main__":
    clients = []
    stocks = []
    
    cashAvailable = 100000
    numDiffStocks = 5
    numClients    = 2
    textFileName  = "someName.txt"
    
    #initialize clients
    for i in range(numClients):
        tempClient = Client(cashAvailable)
        clients.append(tempClient)
    
    #initialize stocks
    for i in range(numDiffStocks):
        tempStack = Stack()
        getInfo(textFileName,tempStack)
        stocks.append(tempStack)
   
            
    
    
    #print balance and yielding of each client every 10 seconds
    #Assume price information available at client side (stack known)
    #Clients buy/sell and know their balance/yielding
    
    
    
