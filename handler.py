# usr/bin/python3


#import sys
import os
import manager
#sock=sys.argv[1]
hostname="kali.fritz.box"
musthaves={"Method":None,"Protocoll":"HTTP/1.1"}
# arguments that packages must have
replaces={"%22":'"',"%3C":"<","%3E":">","%C2%7A":"§","%20":" "}     # signes that are replaced by the browser

class packin:


	pack_dec=""
	args={}
	errors=[]
	

	def __init__(self,pack):
	
		self.pack_dec=pack
		self.args={}
		self.errors=[]
		
		for i in replaces.keys():
			self.pack_dec.replace(i,replaces[i])
		lines=self.pack_dec.split("\n")
		#set parameters from first line
		temp=lines[0].split(" ")
		if len(temp)!=3:
			# header does not have all three arguments
			self.errors+=[400]
			print(temp)
			return None
		temp=temp+[{}]
		if "?" in temp[1]:
			# the package has a search behind the directorie. It has to be set to search
			ds=temp[1].split("?")
			temp[1]=ds[0]    #directorie
			temp[3]=decparamform(ds[1])    #returns a dictionnary of search keys and arguments
		self.args["Method"]=temp[0]
		self.args["Directorie"]=temp[1]
		self.args["Protocoll"]=temp[2]
		self.args["Search"]=temp[3]
		# end of first line
		for i in lines:  #parameters for rest of lines key:value as in package
			if ": " not in i:
				if i != lines[0] and self.args["Method"] == "POST" and "Formdata" not in self.args.keys():
					params=decparamform(i)
					if params!={}:
						self.args.update({"Formdata":decparamform(i)})	# formdata has same format as search
				continue
			temp=i.split(": ")
			self.args[temp[0]]=temp[1]
	
	
	def control(self,musthaves):
		print("-->>controll")
		for i in musthaves.keys():
			if not self.getarg(i):
				self.errors+=[420]
			#elif self.args[i]!=musthaves[i] and musthaves[i]!=None:
			#	print(self.args[i]+"\n"+musthaves[i]+"")
			#	print("-->>Adding ERROR 409")
			#	self.errors+=[409]
		if self.getarg('Method')=="POST" and not self.getarg("Formdata"):
			self.errors += [420]
		return self.errors
	
	def getarg(self,arg):#return argument or False
		if arg in self.args.keys():
			return self.args[arg]
		else:
			return False
	

class packout:
	
	data=b""
	args={}
	header={}
	
	def __init__(self):
		data=b""
		args={}
		return None
	
	def parseheader(self,arguments):
		self.header["Version"]=arguments.pop("Version")
		self.header["Statusnr"]=arguments.pop("Status")
		self.args = arguments
	
	def parsedata(self,data):
		self.data += data
		
	

def go(inp):
	print(">> hanlder: recieved package")
	pack=packin(inp)
	if pack.control(musthaves)!=[]:
		for i in pack.errors:
			print(">> handling error: "+str(i))
		return pack.errors[0]
	outargs=manager.go(pack)
	outpack=packout()
	outpack.parseheader(outargs[1])
	outpack.parsedata(outargs[0])
	return outpack
	



def decparamform(parastring):
	# the parameterstring will be called search here
	params={}
	spsearch=parastring.split("&")    #different search arguments
	for i in spsearch:    #update key:parameter dictionnary
		a=i.split("=")
		if len(a)==2:
			params.update({a[0]:a[1]})
	
	return params
	
	







