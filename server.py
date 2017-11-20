import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = (socket.gethostname(), 10000)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print >>sys.stderr, 'waiting for a connection'
    connection, client_address = sock.accept()

    try:
        print >>sys.stderr, 'connection from', client_address

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(2044)
            print >>sys.stderr, 'received "%s"' % data
            operation = data.split()

            #Transaction failure of 10% here
            if operation[0] == "BUY":
                stock_name = operation[2]
                num_shares = operation[3]
                pper_share = operation[4]
                #Z% probability to buy
                #Update balance and what has been bought
                #Find out what to send back
                print >>sys.stderr, 'sending data back to the client'
                connection.sendall(data)
            elif operation[0] == "SELL":
                #Sell if stock increased by X% || if stock decreased by Y%
                #Issue how to know original buy value? ..
                #Solution? Maybe implement this check client side?
                #Solution? Server keeps track of each stocks buy and sell history? 
                #Update balance and what has been bought
                #Find out what to send back
                print >>sys.stderr, 'sending data back to the client'
                connection.sendall(data)
            else:
                #Error?
                print >>sys.stderr, 'Error: data format inccorect'
                break
            
    finally:
        # Clean up the connection
        connection.close()
