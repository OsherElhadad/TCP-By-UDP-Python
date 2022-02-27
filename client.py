import socket
import sys

# Check if the string is a valid ip.
def is_valid_ip(ip_addr):
	
	# Check if the ip has 4 parts of strings between the dots.
	if len(ip_addr.split('.')) != 4:
		return False

	# Check if the ip has 4 parts of int 0-255.
	for num in ip_addr.split('.'):
		if int(num) < 0 or int(num) > 255:
			return False

	return True

# Check if the argv is valid- 4 argvs, port between 0-65535 and the ip is valid.
if len(sys.argv) == 4 and 0 <= int(sys.argv[1]) <= 65535 and is_valid_ip(sys.argv[2]):
	
	# Get the argvs from the command line.
	this_name, port, ip, file_name = sys.argv
	s = None
	text_file = None
	
	# Try to open a socket and a text file.
	try:
		
		# Open an udp socket with ipv4.
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		
		# Open a text file and reads bytes.
		text_file = open(file_name, "rb")
		
		# Read 96 bytes from the text file.
		data = text_file.read(96)
		text_dict = {}
		
		# The first char is 1 if it's the last massage or 0 else, and the 3 other chars are the index number.
		count = '0000'

		# A loop that adds massages to a dict.
		while data:
			
			# Add 1 to the counter and adds 0 from left until there are 3 digits.
			count = '00' + str(int(count) + 1)
			count = count[len(count) - 3:len(count)]
			
			# Create a massage from 0, count (3 digit) and the text data.
			text_dict[count] = '0' + count + data.decode('utf-8')
			data = text_file.read(96)

		# Replace the first char in the last massage to 1.
		last_text = text_dict.get(count)
		text_dict[count] = last_text.replace('0', '1', 1)
		
		# The number of massages is the current count.
		dict_size = int(count)
		s.settimeout(0.01)

		# A loop that send the all massages and gets back an accept massage for all of them.
		while dict_size != 0:
			for i in sorted(text_dict):
				
				# If this massage didn't accepted back (is None) then we send it again.
				if text_dict[i] is not None:
					s.sendto(bytes(text_dict[i], 'utf-8'), (ip, int(port)))
				try:
					
					# Try to recieve accept massage (3 chars- the number of the massage.
					data, addr = s.recvfrom(3)
					
					# Checks if the recieved massage hasn't accepted already (is not None)- turns it to none.
					if text_dict[data.decode('utf-8')] is not None:
						text_dict[data.decode('utf-8')] = None
						
						# decrease the dict size by 1- we recieved a new massage.
						dict_size = dict_size - 1
				except:
					pass
		text_file.close()
		s.close()
	except:
		if text_file is not None:
			text_file.close()
		if s is not None:
			s.close()
