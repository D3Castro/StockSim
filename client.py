import socket
import sys

class Client:
    __init__(self,cashAvailable):
        self.wallet = cashAvailable
        self.owned  = []
 
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
def buy(client,stock,numStocks,price):
    #AF_INET for ipv4, .6 for ipv6
    try:
        clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    except socket.error,msg:
        print "failed. error code: "+ str(msg[0])+ " and error msg = "+msg[1]
        sys.exit()
    serverIP = "192.168.1.11"
    
    clientSocket.connect((serverIP,2044))
    
    clientSocket.sendall("BUY  "+stock+" "+numStocks+" "+price)    
    #should receive message saying  buy/sell success
    recvMsg = clientSocket.recv(4096) 
    print "recieved message = ",recvMsg
    clientSocket.close()
def sell(client,stock,numStocks,price):
    #AF_INET for ipv4, .6 for ipv6
    try:
        clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    except socket.error,msg:
        print "failed. error code: "+ str(msg[0])+ " and error msg = "+msg[1]
        sys.exit()
    serverIP = "192.168.1.11"
    
    clientSocket.connect((serverIP,2044))
    
    clientSocket.sendall("SELL "+stock+" "+numStocks+" "+price)    
    #should receive message saying  buy/sell success
    recvMsg = clientSocket.recv(4096) 
    if(recvMS == "fail"):
        print "error occured with transaction"
    else:
        print recvMsg
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
    #100,000 cash to spend
    for i in range(2):
        tempClient = Client(100,000)
        clients.append(tempClient)
    #Clients initialized
    
    #stocks = getInfo()
    
    #print balance and yielding of each client every 10 seconds
    #each client sleeps for 1 seconds after comple
    
    
    
    
    
