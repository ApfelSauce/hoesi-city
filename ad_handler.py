# usr/bin/python3

import dbmanager
import shelve
import ssl
from ast import literal_eval

musthaves={"Method":None,"Protocoll":"ADMIN/1.0","Name":None,"Key":None,"Value":None}
login={"bene":"gerhard","ali":"sen","julius":"schreiber"}
cfile= "timefile.s"
# arguments that packages must have
replaces={"%22":'"',"%3C":"<","%3E":">","%C2%7A":"§","%20":" "}     # signes that are replaced by the browser

class packin:
	
	pack=b""
	pack_dec=""
	args={}
	errors=[]
	

	def __init__(self,pack):
		# decode package,write parameters to args
		self.pack=pack
		self.pack_dec=""
		self.args={}
		self.errors=[]
		try:
			self.pack_dec=pack.decode()
		except UnicodeDecodeError:
			self.errors+=["E3 Unencodeable"]
			return None
		for i in replaces.keys():
			self.pack_dec.replace(i,replaces[i])
		lines=self.pack_dec.split("\r\n")
		#set parameters from first line
		temp=lines[0].split(" ")
		if len(temp)!=3:
			# header does not have all three arguments
			self.errors+=["E5 Error with header"]
			return None
		self.args["Method"]=temp[0]
		self.args["Directorie"]=temp[1]
		self.args["Protocoll"]=temp[2]
		# end of first line
		for i in lines:  #parameters for rest of lines key:value as in package
			if ": " not in i:
				continue
			temp=i.split(": ")
			self.args[temp[0]]=temp[1]
	
	
	def control(self,musthaves):
		for i in musthaves.keys():
			if not self.getarg(i):
				self.errors+=["E1 missing argument '"+i+"'"]
			elif self.args[i]!=musthaves[i] and musthaves[i]!=None:
				self.errors+=["E2 argument '"+i+"' has value '"+self.args[i]+"'"]
			else:
				continue
			return self.errors
		if self.args["Name"] in login.keys():
			if self.args["Key"] == login[self.args["Name"]]:
				return []
		return ["wrong login"]
	
	def getarg(self,arg):#return argument or False
		if arg in self.args.keys():
			return self.args[arg]
		else:
			return False
	

class packout:
	
	pack=b""
	
	def __init__(self):
		return None
	
	def parseheader(self,arguments):
		self.pack += (arguments.pop("Version")+" "+arguments.pop("Status")).encode()
		self.pack += b"\r\n"
		for i in arguments.keys():
			self.pack += (i+": "+arguments[i]+"\r\n").encode()
		self.pack+=b"\r\n"
	
	def parsedata(self,data):
		self.pack += data
		
	

def handle(sock):
	print("executing")
	print("\n")
	sock.settimeout(5)
	try:
		sock=ssl.SSLSocket(sock=sock,certfile="cert/public.pem",keyfile="cert/private.pem",server_side=True,ssl_version=ssl.PROTOCOL_TLSv1_2)
		sock.do_handshake()
		inp=sock.recv(1000)
		print(">> adhanlder: recieved package")
		pack=packin(inp)
		if pack.control(musthaves)!=[]:
			for i in pack.errors:
				print(">> adhandling error: "+i)
			return None
		if pack.args["Method"]=="GET":
			sock.send(streamer(pack).pack)
		elif pack.args["Method"]=="WRITE":
			sock.send(execute(pack).pack)
		elif pack.args["Method"]=="SET":
			sock.send(seta(pack).pack)
		dbmanager.save()
	except:
		print("SERVERERROR, sent error message")
	sock.close()
	
	



def decparamform(parastring):
	# the parameterstring will be called search here
	params={}
	spsearch=parastring.split("&")    #different search arguments
	for i in spsearch:    #update key:parameter dictionnary
		a=i.split("=")
		if len(a)==2:
			params.update({a[0]:a[1]})
	
	return params
	
	

def streamer(pack):
	out= packout()
	try:
		rtime = float(pack.args["Value"])
	except ValueError:
		out.parseheader({"Version":"ADMIN/1.0","Status":"400 Bad Request","Error":"time is string"})
		return out
	out.parseheader({"Version":"ADMIN/1.0","Status":"200 OK"})
	rea = dbmanager.safedb.execute("select * from transfers where time > "+ str(rtime))
	reb = rea.fetchmany(100)
	out.parsedata(str(reb).encode())
	return out
	
def execute(pack):
	out= packout()
	try:
		rea = dbmanager.database.execute(pack.args["Value"])
		reb = rea.fetchmany(100)
	except:
		out.parseheader({"Version":"ADMIN/1.0","Status":"400 Bad Request","Error":"invalid command"})
		return out
	out.parseheader({"Version":"ADMIN/1.0","Status":"200 OK"})
	out.parsedata(str(reb).encode())
	return out
	
def seta(pack):
	out= packout()
	if not (pack.getarg("SKey") and pack.getarg("Value")): # pack has to have a key and a value that will be written to the controll file
		out.parseheader({"Version":"ADMIN/1.0","Status":"400 Bad Request","Error":"missing arguments"})
		return out
	a= shelve.open(cfile)
	try:
		value=literal_eval(pack.args["Value"]) # moneygroups has to be tuple
		a.update({pack.args["SKey"]:value})
		print("updated "+ pack.args["SKey"]+"to   "+str(value))
	except:
		print("error concerning the safe file")
	a.close()
	out.parseheader({"Version":"ADMIN/1.0","Status":"200 OK"})
	return out
	






