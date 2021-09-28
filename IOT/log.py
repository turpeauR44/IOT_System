from datetime import datetime

appli_log_path = ""
appli_Debug = False

def init_appli_log_path(hostname):
	global appli_log_path
	appli_log_path = "/home/{}/log.txt".format(hostname)

def write(txt, end=True, timestamp = True):
	if timestamp : txt="{}: {} ".format(datetime.now(),txt)
	if end: txt+="\n"
	with open(appli_log_path,'a+') as Log_file:
		Log_file.write(txt)
		Log_file.close() 
		
		
def init_debug_value(Debug):
	global appli_Debug
	appli_Debug = Debug
	
def return_Debug():
	return appli_Debug
	
'''
class Application_Log:
	def __init__(self,host_name):
		self.path="/home/{}/log.txt".format(host_name)
		self.debug = False
		
	def update_debug(self,Debug):
		self.debug = Debug
		
	def write(self,txt,end=True):
		txt="{}: {} ".format(datetime.now(),txt)
		if end: txt+="\n"
		with open(self.path,'a+') as Log_file:
			Log_file.write(txt)
			Log_file.close() 
'''
