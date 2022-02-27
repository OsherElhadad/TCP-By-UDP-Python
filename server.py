import socket
import sys

# Check if the argv is valid- 2 argvs, port between 0-65535.
if len(sys.argv) == 2 and 0 <= int(sys.argv[1]) <= 65535:
    port = sys.argv[1]
    s = None
    
    # Try to open a socket
    try:
        
        # Open an udp socket with ipv4.
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # Bind the port to the socket.
        s.bind(('', int(port)))

        text_dict = {}
        
        # A flag that turns to the index of a massage only if it is the last massage.
        count = -1

        # A loop that recieve massage and send it's index (3 digits) back for accept.
        while True:
            data, addr = s.recvfrom(100)
            text_dict[data[1:4]] = data[4:100]
            s.sendto(bytes(data[1:4]), addr)

            # Turn count to the index of a massage only if it is the last massage.
            if int(data.decode('utf-8')[0]) == 1:
                count = int(data[1:4].decode('utf-8'))
                
            # If we got the whole massages then we print them in the right order.
            if count == len(text_dict.keys()):
                for key in sorted(text_dict):
                    print(text_dict[key].decode('utf-8'), end="")
                text_dict = {}
                
                # Turn count back to -1 so we won't print the massages again.
                count = -1
    except:
        if s is not None:
			s.close()
