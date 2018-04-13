# usr/bin/python3

import os
import dbmanager
from time import ctime
from http_err import *

dbfile = "database.db"
webdir = 'website'
logindir = webdir



def go(pack):
	if pack.args['Directorie'] == '/puplogin.html':
		print(">> manager: handle pack as pupil")
		manager = pupilmanager(pack)
		packtype = 1
	elif pack.args['Directorie'] == '/storelogin.html':
		print(">> manager: handled pack as store")
		manager = storemanager(pack)
		packtype = 2
	else:
		print(">> manager: handled pack as normal")
		manager = normalreq(pack)
		packtype = 4
	
	status= manager.control()  # control function return http status codes
	if status==200:  # 200 is OK
		print("all right")
		out = manager.execute()
	else:
		print(">> manager: control returned "+str(status))
		manager = normalreq(pack)
		status = manager.control()
		if status==200:
			print("works 2nd time")
			out=manager.execute()
		else:
			return (b"<html><body>error</body></html>",{"Version":"HTTP/1.1","Status":status})
	dbmanager.save()
	return (out,{"Version":"HTTP/1.1","Status":200})
	



class pupilmanager:
	
	rtype=""
	subhandler=0
	
	
	def __init__(self,pack):
		
		
		if pack.getarg("Cookie") and pack.args["Method"]=="POST":  # request of store to be payed by pupil
			self.rtype = 'store book'
			self.subhandler = _storebook(pack)
		elif pack.getarg("Cookie") and pack.args["Method"]=="GET":  # request to get paying formular
			self.rtype = 'store request'
			self.subhandler = _storereq(pack)
		elif pack.args["Method"]=="POST":#request of pupil to get information on his account
			self.rtype="pupil account"
			self.subhandler = _pupilaccount(pack)
		else :# request to get the pupils login side
			self.rtype="pupil request"
			self.subhandler = normalreq(pack)
		
	
	
	def control(self):
		return self.subhandler.control()
	
	
	def execute(self):
		return self.subhandler.execute()
	
	
class _storereq:
	# used to get the paying formular of stores/pupils
	pid=0   # pupils id
	gid=0   # stores id
	gpw=0   # stores password (none of them corrected)
	error = 200
	
	def __init__(self,pack):
		self.error = 200
		cookie = cookiesplit(pack.args["Cookie"]) # returns tuple of all keys and values in cookie, cant fail
		if "id" in cookie.keys() and "pw" in cookie.keys():# store has to send id and password
			self.gid = getintof(cookie["id"])
			self.gpw = getintof(cookie["pw"])
		else:
			self.error = 420
		
		if "id" in pack.args["Search"].keys():# store has to send pupils id
			self.pid = getintof(pack.args["Search"]["id"])
		else:
			self.error = 420
		
	def control(self):
		if self.error != 200:
			return self.error
		if dbmanager.check("store",self.gid,self.gpw) and dbmanager.isin("pupil","id",str(self.pid)):
			return 200
		else:
			return 403
			
		
	
	def execute(self):
		a = open(logindir+"/pupbook.html", 'r')
		b = a.read()
		b = b.replace('<!- Name store -!>',dbmanager.getgname(self.gid))
		a.close
		return b.encode()

class _storebook:
	# used for a paying pupil
	pid=0  # pupils id
	ppw=0  # pupils password
	gid=0  # stores id
	gpw=0  # stores password (none of them corrected)
	money=0
	error = 200
	
	def __init__(self,pack):
		
		self.error = 200
		cookie = cookiesplit(pack.args["Cookie"]) # returns tuple of all keys and values in cookie, cant fail
		if "id" in cookie.keys() and "pw" in cookie.keys() and 'id' in pack.args["Formdata"].keys() and 'pw' in pack.args["Formdata"].keys() and 'money' in pack.args["Formdata"].keys():
			self.pid = getintof(pack.args["Formdata"]["id"])
			self.ppw = getintof(pack.args["Formdata"]["pw"])
			self.gid = getintof(cookie["id"])
			self.gpw = getintof(cookie["pw"])
			self.money = getintof(pack.args['Formdata']['money'])
		else :
			self.error = 420
			return None
			
		
	
	def control(self):
		if self.error != 200:
			return self.error
		if dbmanager.check("pupil",self.pid,self.ppw) and dbmanager.check("store",self.gid,self.gpw):
			return 200
		else:
			return 403
	
	
	def execute(self):
		a = open(logindir+"/bookreaction.html",'r')
		b = a.read()
		a.close()
		b = b.replace('<!- ID pupil -!<',str(self.pid))
		b = b.replace('<!- Name store -!>',dbmanager.getgname(self.gid))
		b = b.replace('<!- ID store -!>',str(self.gid))
		if dbmanager.transfer(('pupil',self.pid),('store',self.gid),self.money):
			b = b.replace('<!- Status transfer -!>','Geld &uuml;berwiesen')
		else:
			b = b.replace('<!- Status transfer -!>','&Uuml;berweistung fehlgeschlagen!')
		return b.encode()
	
class normalreq:
	# can be used for 'normal' requests or requests to get the pupils loginside
	filename=""
	error = 200
	
	def __init__(self,pack):
		self.error = 200
		self.filename = webdir+"/"+pack.args["Directorie"]
		if self.filename.endswith('/'):
			self.filename += 'index.html'
		
	
	def control(self):
		if self.error!=200:
			return self.error
		if os.path.isfile(self.filename) and os.path.commonpath([self.filename,webdir]) == webdir:
			return 200
		else:
			return 404
		
	def execute(self):
		a=open(self.filename,"br")
		b=a.read()
		a.close()
		return b
	


class _pupilaccount:
	# used by pupil to get the accounts state
	pid=0
	ppw=0
	error=200
	
	def __init__(self,pack):
		error = 200
		if "id" in pack.args["Formdata"].keys() and "pw" in pack.args["Formdata"].keys():
			self.pid = getintof(pack.args["Formdata"]['id'])
			self.ppw = getintof(pack.args['Formdata']['pw'])
		else:
			error = 420
	
	def control(self):
		if self.error != 200:
			return self.error
		if dbmanager.check("pupil",self.pid,self.ppw):
			return 200
		else:
			return 403
			
	def execute(self):
		a=open(logindir+'/pupil_account.html','r')
		b=a.read()
		a.close()
		b = b.replace("<!- ID pupil -!>", str(self.pid))
		b = b.replace('<!- money pupil -!>',str(dbmanager.getmoney("pupil",self.pid)).split(".")[0])
		table = dbmanager.sfile.execute('select money, destination, time from transfers where origin = "'+str(self.pid)+'" and otype=0 order by id desc;').fetchmany(10)
		out = '<table class="history" id="history"><tr><td>Summe</td><td>empf&auml;nger</td><td>Zeitpunkt</td></tr>'
		for i in table:
			out+= '<tr><td>'+str(i[0])+'</td><td>'+str(i[1])+'</td><td>'+ctime(i[2])+'</td></tr>'
		out += '</table>'
		b = b.replace('<!- Uberweisungsgeschichte pupil -!>',out)
		return b.encode()
	
class storemanager:
	# manage stores loginpage
	getreq = False
	error = 200
	gid = 0
	gpw = 0
	
	def __init__(self,pack):
		self.error=200
		if pack.getarg("Cookie"):
			cookie = cookiesplit(pack.args['Cookie'])
			if 'id' in cookie.keys() and 'pw' in cookie.keys():
				self.gid = getintof(cookie['id'])
				self.gpw = getintof(cookie['pw'])
				return None
		
		self.error = 420  # control(self) will return False -> if its a login request it will be handled again as normal
		
	def control(self):
		if self.error != 200:
			return self.error
		if dbmanager.check('store',self.gid,self.gpw):
			return 200
		else:
			return 403
	
	def execute(self):
		a=open(logindir+'/store_account.html','r')
		b=a.read()
		a.close()
		name = dbmanager.getgname(self.gid)
		b = b.replace("<!- ID group -!>", str(self.gid))
		b = b.replace('<!- Name group -!>',name)
		b = b.replace('<!- money group -!>',str(dbmanager.getmoney("store",self.gid)))
		return b.encode()
	



def cookiesplit(cookie):
	# return dictionnary of cookie keys and arguments
	# cant fail
	citems=cookie.split("; ")
	datadict={}    # dict where id and password of store and pupil will be saved
	for i in citems:
		a=i.split("=")
		if len(a) == 2:
			datadict.update({a[0]:a[1]})
	return datadict


def getintof(val):
	try:
		return int(val)
	except ValueError:
		return 0


