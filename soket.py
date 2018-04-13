# /usr/bin/python3
import time

class soket:
	def __init__(self):
		pass
		
	def bind(self,addr):
		pass
	
	def listen(self,num):
		pass
		
	def accept(self):
		time.sleep(1)
		return (soket(),)
		
	def recv(self,size):
		print("socket: please insert package with len "+str(size))
		print("\n\n\n")
		a=input().replace(r"\r\n","\r\n").encode()
		return a
	
	def send(self,pack):
		print(pack.decode())
		print("\n\n\n")
		
	def close(self):
		print("end")
