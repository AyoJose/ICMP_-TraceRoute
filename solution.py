import socket
from socket import gethostbyname
import os
import sys
import struct
import time
import select
import binascii
import math
 
ICMP_ECHO_REQUEST = 8
MAX_HOPS = 30
TIMEOUT = 2.0
TRIES = 2

# The packet that we shall send to each router along the path is the ICMP echo
# request packet, which is exactly what we had used in the ICMP ping exercise.
# We shall use the same packet that we built in the Ping exercise
 
def checksum(string):
    csum = 0
    countTo = (len(string) // 2) * 2
    count = 0
 
    while count < countTo:
        thisVal = (string[count + 1]) * 256 + (string[count])
        csum += thisVal
        csum &= 0xffffffff
        count += 2
 
    if countTo < len(string):
        csum += (string[len(string) - 1])
        csum &= 0xffffffff
 
    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer
 
def build_packet():
    #Fill in start
    # In the sendOnePing() method of the ICMP Ping exercise ,firstly the header of our
    # packet to be sent was made, secondly the checksum was appended to the header and
    # then finally the complete packet was sent to the destination.
    # Make the header in a similar way to the ping exercise.
    # Append checksum to the header.
    # Don’t send the packet yet , just return the final packet in this function.
    #Fill in end
    # So the function ending should look like this
    myChecksum = 0 
    pid = os.getpid() & 0xFFFF
    header = struct.pack('bbHHh', ICMP_ECHO_REQUEST, 0, myChecksum,pid,1)
    data = struct.pack('d', time.time())
    myChecksum = checksum(header+data)	
    if sys.platform == 'darwin': 
        myChecksum = socket.htons(myChecksum) & oxffff
	
    else: 
        myChecksum = htons(myChecksum)
	
 
    packet = header + data
    return packet
 
def get_route(hostname):
    timeLeft = TIMEOUT
    print('starting here;')
    tracelist1 = [] #This is your list to use when iterating through each trace 
    tracelist2 = [] #This is your list to contain all traces
    icmp = socket.getprotobyname('icmp') 
    for ttl in range(1,MAX_HOPS):
        print('for loop starts here') 
        tracelist1 = [] 
        for tries in range(TRIES):
            destAddr = socket.gethostbyname(hostname) 
            #Fill in start
            # Make a raw socket named mySocket
            mySocket = socket.socket(socket.AF_INET,socket.SOCK_RAW,icmp)
            #Fill in end
 
            mySocket.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, struct.pack('I', ttl))
            mySocket.settimeout(TIMEOUT)
            print('debug part 1' ) 
            try:
                d = build_packet()
		#hello = 5 
                mySocket.sendto(d, (hostname, 0))
                t= time.time()
                startedSelect = time.time()
                whatReady = 10# select.select([mySocket], [], [], timeLeft)
                #print(whatready) 		
                howLongInSelect = 10 #(time.time() - startedSelect)
                if whatReady[0] == []: # Timeout
                    #tracelist1=(tries,'*',"* * * Request timed out.")
                    print('*** Request timed out.') 
                    #Fill in start
                    #tracelist2 = tracelist2.append(tracelist1) 
                    #You should add the list above to your all traces list
                    #Fill in end
                recvPacket, addr = mySocket.recvfrom(1024)
                timeReceived = time.time()
                timeLeft = 20 #timeLeft - howLongInSelect
                #print('debug part 2') 
                #print(timeLeft) 
                if timeLeft <= 0:
                    #tracelist1.append("* * * Request timed out.")
                    #Fill in start
                    #tracelist1=(tries,'*',"* * * Request timed out.")
                    print('*** Request timed out.') 
                    #Fill in start
                    #tracelist2 = tracelist2.append(tracelist1) 
                    #print('*** Request timed out.')
                    #You should add the list above to your all traces list
                    #Fill in end
                    #print('debug part 2.5') 
            except:
                continue
 
            else:
                print('2.9') 
                #Fill in start
                #Fetch the icmp type from the IP packet
                icmp_header = recvPacket[20:28] 
                type,code,checksum,pid,sequence = struct.unpack('bbHHh', icmp_header) 
                #Fill in end
                #try:
                    #host_Name = socket.gethostbyaddr(destAddr) 
                    #Fill in start
			
                    #Fill in end
                #except host_Name[0] == []:   #if the host does not provide a hostname
                    #Fill in start
                    #host_Name = 'hostname not returnable' 
                    #Fill in end
			
                if type == 11:
                    bytes = struct.calcsize("d")
                    timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
                    #Fill in start
                    #You should add your responses to your lists here
                    #tracelist1.append('%d , %d, %struct, %s' %(ttl, (timeReceived - timeSent)*1000, addr[0]),host_Name)
                    print('debug part 3 ') 
                    print('%d rtt= %.0f ms %s' %(ttl, (timeReceived - t)*1000, addr[0]))			
                    #Fill in end
                elif type == 3:
                    bytes = struct.calcsize("d")
                    timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
                    #Fill in start
                    #You should add your responses to your lists here 
                    #tracelist1.append('%d , %d, %struct, %s' %(ttl, (timeReceived - timeSent)*1000, addr[0]),host_Name)
                    print('debug part 4 ') 
                    print('%d rtt= %.0f ms %s' %(ttl, (timeReceived - t)*1000, addr[0]))
                    #Fill in end
                elif type == 0:
                    bytes = struct.calcsize("d")
                    timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
                    #Fill in start
                    #tracelist1.append('%d , %d, %struct, %s' %(ttl, (timeReceived - timeSent)*1000, addr[0]),host_Name)
                    #You should add your responses to your lists here and return your list if your destination IP is met
                    print('debug part 5 ')
                    print('%d rtt= %.0f ms %s' %(ttl, (timeReceived - t)*1000, addr[0])) 
                    #Fill in end
                    return
                else:
                    #Fill in start
                    #If there is an exception/error to your if statements, you should append that to your list here
                    print('error')
                    print('debug part 6 ') 
                    break
                    #Fill in end
         
            finally:
                mySocket.close()
