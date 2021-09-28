#! /usr/bin/python3
import paramiko
try:
	import serial
except:
	print('no serial module')
import json
from datetime import datetime, timedelta
import time
import pytz
import sys
from os import makedirs, listdir, remove
from os.path import isfile, join, exists, getmtime
import subprocess
import numpy as np

Twodigits=lambda x: x if x>9 else '0{}'.format(x)
date_strip1 = lambda date_txt: datetime.strptime(date_txt,"%Y-%m-%dT%H:%M:%S")
datefile = lambda date: "{}{}{}_".format(date.year-2000,Twodigits(date.month),Twodigits(date.day))
date_js = lambda date : "{}-{}-{} {}:{}:{}".format(date.year,Twodigits(date.day),Twodigits(date.month),Twodigits(date.hour),Twodigits(date.minute),Twodigits(date.second))

def date_sh(mydatetime = datetime.now(), tz=0):
	mydatetime = mydatetime - timedelta(hours=tz)
	return "{}{}{}{}{}".format(Twodigits(mydatetime.month),Twodigits(mydatetime.day),Twodigits(mydatetime.hour),Twodigits(mydatetime.minute),mydatetime.year-2000)
		
def date_now():
	return datetime.utcnow().replace(tzinfo=pytz.utc)


def get_average(List):
	return np.average(List)
	
def get_max(List):
	return np.max(List)

def create_user_client_upload_bash(user, client, bash_file):
	Dico={"User_addr":user.hostname, "User_password" : user.password, "Client_addr": client.host, "Client_password" : client.password}
	subprocess.run("echo #!/bin/bash >> {}".format(bash_file), shell = True)
	for key, value in Dico:
		subprocess.run("echo {} = {} >> {}".format(key,value,bash_file),shell=True)

def get_files(mypath, delimit=False):
	try:
		return [tuple(f.split('.')) for f in listdir(mypath) if isfile(join(mypath, f))]
	except:
		return []
		
def remove_file(mypath):
	remove(mypath)

def get_json(myfile):
	with open(myfile,'r') as json_file:
		data=json.load(json_file)
		json_file.close()
	return data

def create_ssh_client():
	ssh_client	=paramiko.SSHClient()
	ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	return ssh_client

def get_or_create_json(myfile,init=[]):
	if isfile(myfile):
		return get_json(myfile)
	else:
		with open(myfile,'w') as json_file:
			json_file.write(json.dumps([]))
			json_file.close()
		return get_json(myfile)

def get_or_create_jsonlist(myfile):
	if isfile(myfile):
		return get_json(myfile), False
	else:
		with open(myfile,'w') as json_file:
			json_file.write(json.dumps([]))
			json_file.close()
		return json.loads(json.dumps([])), True
		

def create_json(myfile, dico):
	with open(myfile,'w') as json_file:
		json_file.write(json.dumps(dico))
		json_file.close()
		
def append_json(myfile, dico):
	with open(myfile,'a+') as json_file:
		json_file.write(json.dumps(dico))
		json_file.close()
	
def create_folder(path, dday=False, dmonth=False, return_path = False):
	'''
	dday au format date permet de créer une arborescence de date
	stop_month: permet de stocker des fichier au niveau du mois
	'''
	if dday:
		date_liste = [dday.year-2000,Twodigits(dday.month),Twodigits(dday.day)]
		if dmonth:
			path = "{}/{}/{}".format(path,*date_liste)
		else:
			path = "{}/{}/{}/{}".format(path,*date_liste)
	
	if not exists(path): makedirs(path)
	
	if return_path:
		return path
			
		
def remove_file(path):
	if exists(path): remove(path)

def datetime_mod(myfile):
	return datetime.strptime(time.ctime(getmtime(myfile)), "%a %b %d %H:%M:%S %Y")

def transformed_data(data):
	if data == '': return []
	return [int(val) for val in data.split(',')]
	
def controller_com(mycontroller):
	com = serial.Serial(mycontroller.obj.serial, mycontroller.obj.baud)
	time.sleep(2)
	return com

def controller_write(mycontroller,code):
	mycontroller.com.write(str(code).encode())
	
def controller_write_read(mycontroller,code):
	mycontroller.com.write(str(code).encode())
	time.sleep(0.1)
	return controller_read(mycontroller)

def controller_read(mycontroller):
	return '{}'.format(mycontroller.com.readline()).replace("b'","").replace("\\r\\n'","")

def reject_outlier(array, m=0.5, win=3):
	array_corr=np.copy(array)
	d = np.abs(array- np.median(array))
	mdev = np.median(d)
	idxs_outliers = np.nonzero(d>m*mdev)[0]
	for i in idxs_outliers:
		if i-win <0:
			array_corr[i] = np.median(np.append(array[0:i], array[i+1:i+win+1]))
		elif i+win+1 >len(array):
			array_corr[i] = np.median(np.append(array[i-win:i], array[i+1:len(array)]))
		else:
			array_corr[i] = np.median(np.append(array[i-win:i], array[i+1:i+win+1]))
	return array_corr
			
def exec_command(cmd):
	subprocess.run(cmd,shell=True)

def synchro_required(date_os_client):
	date_os_client= date_strip1(date_os_client)
	return abs(date_os_client-datetime.now())>timedelta(microseconds=60)

def synchro_date_required(date_client, date_ref):
	return abs(date_client-date_ref)>timedelta(microseconds=60)
'''
	def create_loads_bash(self, init=False):
		self.create_upload_bash(init)

	def create_upload_bash(self, init):
		print('creation du bash upload vers master')
		with open("bash/upload.config",'w') as upload_file:
			upload_file.write("#!/bin/bash\n")
			for key, value in self.__dict__.items():
				if not str(value)[0] in ['<','['] : upload_file.write(' {}="{}"\n'.format(key,value))
			for key, value in self.master.__dict__.items():
				if not str(value)[0] in ['<','['] : upload_file.write(' master_{}="{}"\n'.format(key,value))

'''
