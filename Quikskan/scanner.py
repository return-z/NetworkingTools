#This is a fast port scanner. Works on the principle of threading which
#gives it much faster speeds.
import socket,sys,time,threading,re

active_ports = {}

#function machinery is the backbone and is fed into threading
def machinery(ip,port):
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.settimeout(1)
	try:
		s.connect((ip,port))
		active_ports[port] = 'ON'
	except:
		active_ports[port] = ''

#a function for reading port range in a min-max format
def port_ends(r):
	vals = r.split('-')

	vals[0] = int(vals[0])
	vals[1] = int(vals[1])

	#for bad input
	if vals[1] < vals[0]:
		temp = vals[1]
		vals[1] = vals[0]
		vals[0] = temp

	return vals

#The function that works to thread the machinery
def scan(ip,num_threads,r):
	ends = port_ends(r)
	last_port = ends[1]
	count  = ends[0]
	offset = count

	if last_port > 65535:
		print("Invalid ports! Quitting!")
		main()


	threads = []

	while count <= last_port:
		for i in range(count,count+num_threads):
			t = threading.Thread(target=machinery,args=(ip,i))
			threads.append(t)
			threads[i-offset].start()

		for i in range(count,count+num_threads):
			threads[i-offset].join()

		for i in range(count,count+num_threads):
			if active_ports[i] == 'ON':
				print(f"Port {i} is ON")

		count += num_threads


def main():

	#print welcome banner
	print("""
  /$$$$$$  /$$   /$$ /$$$$$$ /$$   /$$  /$$$$$$  /$$   /$$  /$$$$$$  /$$   /$$      
 /$$__  $$| $$  | $$|_  $$_/| $$  /$$/ /$$__  $$| $$  /$$/ /$$__  $$| $$$ | $$      
| $$  \ $$| $$  | $$  | $$  | $$ /$$/ | $$  \__/| $$ /$$/ | $$  \ $$| $$$$| $$      
| $$  | $$| $$  | $$  | $$  | $$$$$/  |  $$$$$$ | $$$$$/  | $$$$$$$$| $$ $$ $$      
| $$  | $$| $$  | $$  | $$  | $$  $$   \____  $$| $$  $$  | $$__  $$| $$  $$$$      
| $$/$$ $$| $$  | $$  | $$  | $$\  $$  /$$  \ $$| $$\  $$ | $$  | $$| $$\  $$$      
|  $$$$$$/|  $$$$$$/ /$$$$$$| $$ \  $$|  $$$$$$/| $$ \  $$| $$  | $$| $$ \  $$      
 \____ $$$ \______/ |______/|__/  \__/ \______/ |__/  \__/|__/  |__/|__/  \__/      
      \__/                                                                          
                                                                                    
 	""")

	print("<---------------------------------Version (0.1)---------------------------------------------->\n")

	ip = input("Enter the IP Address of the host : ")
	print(f"You entered IP : {ip}\n")

	print("Choose an option : \n 1. Scan for common ports \n 2. Custom scan \n 3. Go Home\n")

	choice = int(input("Your choice : "))


	if choice == 1:
		num_threads = int(input("\nSet the number of threads (1-200) : "))

		if num_threads < 1 or num_threads > 200:
			num_threads = int(input("Please enter a valid number of threads : "))

		else:
			start = time.time()
			r = '1-1000'
			print("\n")
			scan(ip,num_threads,r)
			print(f"\nPort sacn finished! Process completed in {round(time.time()-start,2)} seconds")
			sys.exit()



	elif choice == 2:
		r = input("\nEnter the port range (min-max, eg 1-1000) : ")

		num_threads = int(input("Set the number of threads (1-200) : "))

		if num_threads < 1 or num_threads > 200 :
			num_threads = int(input("Please enter a valid number of threads (1-200) : "))

		else:
			start = time.time()
			print("\n")
			scan(ip,num_threads,r)
			print(f"\nPort scan finished! Process completed in {round(time.time()-start,2)} seconds")
			sys.exit()

	elif choice == 3:
		print("Quitting program!")
		sys.exit()

	else:
		print("Invalid choice. Quitting!")
		sys.exit()

if __name__ == "__main__":

	try:
		main()
	except KeyboardInterrupt:
		print("Quitting program!")
		sys.exit()




		








	