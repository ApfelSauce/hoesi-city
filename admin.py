#! /usr/bin/python3


import socket
import dbmanager
import ad_handler
from time import time
import multiprocessing


hostip="0.0.0.0"
timeout=7 # process that handles request will be killed after this timeout



# initialise server
sock=socket.socket()
sock.bind((hostip,1413)) 
sock.listen(5)
subsockdict={}
def server():
	try:
		while True:
			ctime=time()   #time for controlling request timeout
			a=[]
			for key in subsockdict.keys():
				if not key.is_alive():   # control keeping timeout for all
					a+=[key]
				elif (ctime-subsockdict[key])>timeout:
					key.terminate()   # terminate process if it is alive and didnt keep timeout
					a+=[key]
					print("terminated")
			for key in a:
				del subsockdict[key]   #kill all closed processes
			print("waiting for connection")
			subsock=sock.accept()
			handlesub=multiprocessing.Process(target=ad_handler.handle,args=(subsock[0],))   # handle request in subprocess for not having to wait until its finish
			handlesub.run()
			subsockdict.update({handlesub:time()})   # dictionnary of subprocesses and opening time
	except KeyboardInterrupt:
		sock.close()
		print("ERROR")

server()



