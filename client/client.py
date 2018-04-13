#! /usr/bin/python3

import ssl
import cmd
import pprint
import multiprocessing
import time
from ast import literal_eval
from socket import socket

hostip=("0.0.0.0",1413)


def printtablelayout(table):
	try:
		outt = literal_eval(table)
	except:
		return "invalid table!"
	out=""
	for i in outt:
		pr=""
		for a in i:
			pr+= str(a).ljust(20)
		out += pr
		out += "\n"
	return out

def dotablerequest(send):
	sock= ssl.SSLSocket(sock=socket(),ca_certs="public.pem")
	sock.settimeout(5)
	try:
		sock.connect(hostip)
		sock.send(send)
		data = sock.recv(10000)
	except:
		print("\x1b[44;31mServer is unreachable!\x1b[0m")
		return (("",),)
	sock.close()
	try:
		data = data.decode()
	except UnicodeDecodeError:
		print("Error: undecodeable")
		return (("",),)
	data=data.split("\r\n\r\n")
	if len(data) == 2:
		return data[1]
	else:
		print("no result")
		return (("",),)
		
	
	
	
	
	
class commands(cmd.Cmd):
	
	name="julius"
	key="schreiber"
	skey=""
	prompt="Ich@Hö-Si-Server >  "
	
	def do_execute(self,command):
		b=dotablerequest(("""WRITE / ADMIN/1.0\r
Value: """ +command+ """\r
Name: """ + self.name + """\r
Key: """ + self.key + "\r\n").encode())
		
		a = printtablelayout(b)
		print(a)
		print("\n\n----------------------------------------------------------------------------------------------------------------------------------------------------------------------\n\n")
			
	def do_stream(self,interval):

		print("started streaming")
		
		while True:
			b = dotablerequest(("""GET / ADMIN/1.0\r
Value: """ +str(time.time()-int(interval))+ """\r
Name: """ + self.name + """\r
Key: """ + self.key + "\r\n").encode())
			a = printtablelayout(b)
			print(a)
			time.sleep(int(interval))
			
	def do_set(self,value):
		sock= ssl.SSLSocket(sock=socket(),ca_certs="public.pem")
		sock.settimeout(5)
		try:
			sock.connect(hostip)
			sock.send(b"SET / ADMIN/1.0\r\nSKey: "+self.skey.encode()+b"\r\nValue: "+value.encode()+b"\r\nKey: "+self.key.encode()+b"\r\nName: "+self.name.encode()+b"\r\n")
			data = sock.recv(10000)
		except:
			print("\x1b[44;31mServer is unreachable!\x1b[0m")
			return (("",),)
		sock.close()
			
	def do_setname(self,name):
		self.name = name
	
	def do_setkey(self,key):
		self.key=key
	
	
	def do_setskey(self,key):
		self.skey=key

commander=commands()
commander.cmdloop()
		
				
		
		
	
			
		
		
		
