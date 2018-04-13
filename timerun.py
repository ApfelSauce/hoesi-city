#! /usr/bin/python3
from time import sleep
import dbmanager
import sqlite3
import shutil
import shelve
varpath="timefile.s"
sdir= "safe/"



fnr = 0
moneygroups={}

while True:
	
	
	try:
		varfile=shelve.open(varpath)
		money=int(varfile["lowest"])
		dbmanager.steuer=float(varfile["tax"])
		sleeptime = int(varfile["sleeptime"])
		moneygroups = varfile["moneygroups"]
		print(moneygroups)
		varfile.close()
	
		shutil.copy(dbmanager.dbpath,sdir+dbmanager.dbpath+str(fnr))
		shutil.copy(dbmanager.spath,sdir+dbmanager.spath+str(fnr))
		fnr += 1
		sleep(sleeptime)
		print("running for the "+ str(fnr) + "st time!")
		res = dbmanager.database.execute('select id,money from store')# database used in dbmanager
		stores = res.fetchall()
		for i in stores:
			
			if i[0] in moneygroups.keys():   # grups that dont earn money
				gmoney = i[1] + moneygroups[i[0]]  # add money they get to money they have
				dbmanager.database.execute('update store set money = '+str(gmoney)+' where id = '+str(i[0])+' ;')
		
			pres = dbmanager.database.execute('select pupil.id from pupil,store where store.id = pupil.gid and store.id = "'+str(i[0])+'";')
			pups = pres.fetchall()# list of pupils
			pmoney = int(i[1]/len(pups))# money that each pupil would get
			
			if pmoney < money:# group has too less money to pay workers
				gmoney = i[1] + (money-pmoney)*len(pups)# add as much money as needed to pay all workers
				dbmanager.database.execute('update store set money = '+str(gmoney)+' where id = '+str(i[1])+' ;') #give goup more money
				pmoney=money
			
			for a in pups:
				dbmanager.transfer(('store',i[0]),('pupil',a[0]),pmoney)
		dbmanager.save()
	except:
		pass

