#! /usr/bin/python3
from http.server import BaseHTTPRequestHandler,HTTPServer
import handler

hostip=""
timeout=20 # process that handles request will be killed after this timeout


class handler_class(BaseHTTPRequestHandler):
	def do_GET(self):
		pack="GET "+self.path+" "+self.request_version+"\r\n"+self.headers.as_string()
		print(pack)
		self.myfunction(pack)
		
	def myfunction(self,pack):
		a=handler.go(pack)
		if type(a)==int:
			self.send_error(a)
		else:
			self.send_response(a.header["Statusnr"])
			for i in a.args.keys():
				self.send_header(i,a.args[i])
			self.end_headers()
			self.wfile.write(a.data)
		
	def do_POST(self):
		pack="POST "+self.path+" "+self.request_version+"\r\n"+self.headers.as_string()+"\r\n\r\n"
		if True:
			LEN= int(self.headers.get("content-length"))
			pack+= self.rfile.read(LEN).decode()
			print(pack)
		else:
			print(1)
			pass
		print(pack)
		self.myfunction(pack)
		




# initialise server
httpd = HTTPServer((hostip,8080), handler_class)
httpd.serve_forever()

