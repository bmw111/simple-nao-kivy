import socket  
  
address = ('0.0.0.0', 11112)  
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
s.bind(address)  
  
while True:  
	data, addr = s.recvfrom(2048)  
	if not data:  
		print "client has exist"  
		break  
	print "received:", data, "from", addr  
	print data[:2]
	print data[2:]
  
s.close()  