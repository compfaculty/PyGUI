__author__ = 'alex'
# The discovery process involves sending hex 00 00 00 F8 to UDP 30718.
# If you broadcast this, all Lantronix CobOS (including XPort) will send
# a response that starts with hex 00 00 00 F9.
# The response from each device is exactly 120 bytes and will always start
# with the hex 00 00 00 F9 when the query starts with hex 00 00 00 F8.
# The four hex values immediately after the F9 are the responding unit's IP address in hex.
from socket import *
from sys import *

# ## Set the socket parameters
# host = <ip-define-here>
port = 30718
import select
import socket
import sys
import Queue

# Create a TCP/IP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(0)

# Bind the socket to the port
server_address = ('localhost', 10000)
print >>sys.stderr, 'starting up on %s port %s' % server_address
server.bind(server_address)

# Listen for incoming connections
server.listen(5)
# Sockets from which we expect to read
inputs = [ server ]

# Sockets to which we expect to write
outputs = [ ]
# Outgoing message queues (socket:Queue)
message_queues = {}
while inputs:

    # Wait for at least one of the sockets to be ready for processing
    print >>sys.stderr, '\nwaiting for the next event'
    readable, writable, exceptional = select.select(inputs, outputs, inputs)
     # Handle inputs
    for s in readable:

        if s is server:
            # A "readable" server socket is ready to accept a connection
            connection, client_address = s.accept()
            print >>sys.stderr, 'new connection from', client_address
            connection.setblocking(0)
            inputs.append(connection)

            # Give the connection a queue for data we want to send
            message_queues[connection] = Queue.Queue()
        else:
            data = s.recv(1024)
            if data:
                # A readable client socket has data
                print >>sys.stderr, 'received "%s" from %s' % (data, s.getpeername())
                message_queues[s].put(data)
                # Add output channel for response
                if s not in outputs:
                    outputs.append(s)
            else:
                # Interpret empty result as closed connection
                print >>sys.stderr, 'closing', client_address, 'after reading no data'
                # Stop listening for input on the connection
                if s in outputs:
                    outputs.remove(s)
                inputs.remove(s)
                s.close()

                # Remove message queue
                del message_queues[s]
    # Handle outputs
    for s in writable:
        try:
            next_msg = message_queues[s].get_nowait()
        except Queue.Empty:
            # No messages waiting so stop checking for writability.
            print >>sys.stderr, 'output queue for', s.getpeername(), 'is empty'
            outputs.remove(s)
        else:
            print >>sys.stderr, 'sending "%s" to %s' % (next_msg, s.getpeername())
            s.send(next_msg)
    # Handle "exceptional conditions"
    for s in exceptional:
        print >>sys.stderr, 'handling exceptional condition for', s.getpeername()
        # Stop listening for input on the connection
        inputs.remove(s)
        if s in outputs:
            outputs.remove(s)
        s.close()

        # Remove message queue
        del message_queues[s]
# buf = 1024
# addr = (host,port)
#
# ## Create socket
# UDPSock = socket(AF_INET,SOCK_DGRAM)
#
# ## Send messages
# data ='\x41'
# #data=argv[1] #commented out
# if not data:
#     print "No data"
# else:
#     if(UDPSock.sendto(data,addr)):
#         print "Sending message ",data
#
# ## Close socket
# UDPSock.close()
#
# ###############
# # Send UDP broadcast packets
#
# MYPORT = 50000
#
# import sys, time
# from socket import *
#
# s = socket(AF_INET, SOCK_DGRAM)
# s.bind(('', 0))
# s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
#
# while 1:
#     data = repr(time.time()) + '\n'
#     s.sendto(data, ('<broadcast>', MYPORT))
#     time.sleep(2)
#socket.inet_ntoa(struct.pack(">L", 0xac1b4060))
from socket import *
import struct

START_IP_BYTE = 4
END_IP_BYTE = 8
ask = struct.pack('!I', 0x000000F8)

cs = socket(AF_INET, SOCK_DGRAM)
cs.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
cs.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
cs.sendto(ask, ('172.27.255.255', 30718))
# while True:
#     res = cs.recv(1024)
#     if not res: break
#     ip =  '.'.join([str(x) for x in struct.unpack('!BBBB', res[START_IP_BYTE:END_IP_BYTE])])
#     print ip
#     #print struct.unpack("s", res[4:8])
#     #print inet_ntoa(struct.pack(">L", hex(res[4:7])))


cs.close()
