#! /usr/bin/python3
import sqlite3
from time import time
import shelve


dbpath = "database.db"
dbfile = sqlite3.connect(dbpath)
database = dbfile.cursor()
spath = 'sfile.db'
sfile = sqlite3.connect(spath)
safedb = sfile.cursor()
steuer = 0.99

types=("pupil","store")


def check(table,rid,pw):
	a=database.execute("select * from "+table+" where id='"+str(rid)+"' and pw='"+str(pw)+"';")
	if len(a.fetchmany(4)) == 1:
		return True
		print(">> dbmanager: login verified")
	else:
		print(">> dbmanager: login false")
		return False


def transfer(origin,destination,num):
	a=database.execute("select money,locked from " + origin[0] + " where id = '" + str(origin[1]) + "';").fetchone()[0:2]
	b=database.execute("select money,locked from " + destination[0] + " where id = '" + str(destination[1]) + "';").fetchone()[0:2]
	if int(a[0]) < num or a[1] or b[1] or num < 1:
		return False
	netto = num * steuer
	database.execute("update "+origin[0]+" set money = " + str(a[0]-num) + " where id = '" + str(origin[1]) + "';")
	database.execute("update "+ destination[0] +" set money = " + str(b[0]+netto) + " where id = '" + str(destination[1]) + "';")
	
	safedb.execute("insert into transfers(otype,origin,dtype,destination,money,time) values ('"+ str(types.index(origin[0])) + "','" + str(origin[1]) + "','" + str(types.index(destination[0])) + "','" + str(destination[1]) + "','"+str(num)+"','"+str(time())+"');") # write  to safe database for knowing transactions later
	
	return True
	

def isin(table, column, value):
	# works only with string values
	a=database.execute("select * from "+table+" where " + column +" = '" + str(value) + "';")
	if len(a.fetchmany(4)) >= 1:
		return True
	else:
		return False
	

def getgname(gid):
	a = database.execute('select name from store where id = "'+str(gid)+'";')
	return a.fetchone()[0]

def getmoney(table,rid):
	a = database.execute('select money from '+table+' where id = "'+str(rid)+'";')
	return a.fetchone()[0]

def save():
	global dbfile
	global dbpath
	global database
	
	global spath
	global sfile
	global safedb
	
	database.close()
	safedb.close()
	
	dbfile.commit()
	sfile.commit()
	
	dbfile.close()
	sfile.close()
	
	dbfile = sqlite3.connect(dbpath)
	sfile = sqlite3.connect(spath)
	
	database = dbfile.cursor()
	safedb = sfile.cursor()
	
	a=shelve.open("timefile.s")
	try:
		steuer = float(a["tax"])
	except:
		print(">> dbmanager: updating tax failed")
	
	a.close()
	
