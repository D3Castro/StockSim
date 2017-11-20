import socket
import sys

class Client:
    __init__(self,cashAvailable):
        self.wallet = cashAvailable
        self.owned  = []

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

def getInfo():
    #AF_INET for ipv4, .6 for ipv6
    try:
        clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    except socket.error,msg:
        print "failed. error code: "+ str(msg[0])+ " and error msg = "+msg[1]
        sys.exit()
    serverIP = "192.168.1.11"
    clientSocket.connect((serverIP,2044))
    clientSocket.sendall("INFO")
    
    stocksAvailable = []
    
    data = clientSocket.recv(4096)
    while data:
        #find way to splice the string at each white space
        stockprice = data
        stockName = data
        numStocks = data
        stocksAvailable.append((stockPrice,stockName,numStocks))
    
    clientSocket.close()
    return stocksAvailable
    
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
    
    
    
    
