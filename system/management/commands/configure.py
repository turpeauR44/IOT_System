#! /usr/bin/python3
#	Import des librairies version 6
	#	Standard
import sys
import subprocess
import paramiko
import time

	#	Django
from django.core.management.base import BaseCommand, CommandError

	#	Projet		
from system.models import *
from system.management.functions.txts import *

Path		= "{}/system/management".format(sys.path[0])
Path_files 	= "{}/files".format(Path)
Path_bash 	= "{}/bash".format(Path)

local_files_toexecute=[	'check_internet.sh',
						'mymake.sh', 
						'start_ssh.sh',
						'git_pull.sh',
						'send_ssh_key.sh',
						'transfer_via_ssh.sh',
						'add_line.sh',]
local_files_totransfer=[{'file':'pg_hba.conf', 		'target':'/etc/postgresql/11/main',	'owner_change':'file', 	'functions':['system']},
						{'file':'postgresql.conf', 	'target':'/etc/postgresql/11/main',	'owner_change':'file', 	'functions':['system']},
						{'file':'rc.local', 		'target':'/etc',					'owner_change':'file', 	'functions':['system']},
						{'file':'hostapd.conf', 	'target':'/etc/hostapd',			'owner_change':'dir', 	'functions':['system','bridge']},
						{'file':'hostapd', 			'target':'/etc/default',			'owner_change':'file', 	'functions':['system','bridge']},
						{'file':'hostapd.accept', 	'target':'/etc/hostapd',			'owner_change':'dir', 	'functions':['system','bridge']},
						{'file':'interfaces', 		'target':'/etc/network',			'owner_change':'file', 	'functions':['system','bridge']},
						{'file':'sysctl.conf', 		'target':'/etc',					'owner_change':'file', 	'functions':['system','bridge']},]
services_torestart=[{'service':'postgresql',	'enable':False,	'functions':['system']},
					{'service':'hostapd',		'enable':False, 'functions':['system','bridge']},
					{'service':'dncpd',			'enable':False, 'functions':['system','bridge']},
					]

Target={"method":0,
		"os":None,"host":None,"cpu":None,"bridge":None,"system":None,'network':None,
		'cur_cpu':None,'cur_host_net':None, 
		"user":None,'ipv4':None,'password':None,
		"ssh":None}
apt_packages		={	'git':60, 
						'sshpass':60 ,
						'python3-pip': 90,
						'libatlas-base-dev':30,
						'postgresql':240,
						'sqlite3':120,
						'cryptsetup':120,
						'pv':120 }
apt_packages_bridge	={	'hostapd':120,
						'bridge-utils':60}
pip_packages		={	'psutil':60, 
						'pyserial':120, 
						'numpy':120, 
						'Django': 120,
						'djangorestframework':120,
						'markdown':120,
						'django-filter':120,
						'paramiko':120, 
						'psycopg2':120 }


class Command(BaseCommand):
	help = 'Commande de lancement de la configuration de l\'hôte'
	def add_arguments(self, parser):
		parser.add_argument('-d', dest='debug', action='store_true')
		parser.add_argument('-t', dest='no_down', action='store_true')
		parser.add_argument('-u', dest='no_update', action='store_true')
	def handle(self, *args, **options):
		Processus_OK = step_proceed(initialization,"Initialisation",0, **options)
		if Processus_OK: Processus_OK = step_proceed(select_config_mode,"Choix de la méthode de configuration",1, **options)
		if Processus_OK: Processus_OK = step_proceed(get_target,"Contrôle des détails de la cible",2, **options)
		if Processus_OK and not options['no_down']: Processus_OK = step_proceed(net_downloads,"Téléchargement des paquets nécessaires",3, **options)
		if Processus_OK: Processus_OK = step_proceed(ssh_configuration,"Configuration du ssh",5, **options)
		if Processus_OK: Processus_OK = step_proceed(files_transfert,"Transfert des fichiers de configuration",6, **options)			
		#if Processus_OK: Processus_OK = step_proceed(git_pull,"Git Pull",6, **options)

def step_proceed(function, title, step, **options):
	txt_Step(title, step)
	STEP_OK=function(**options)	
	if not STEP_OK: txt_StepFailed(step)
	print()
	return STEP_OK

def initialization(**options):
	def make_local_files_executable():
		txt_Proceed("Local files management")
		step_ok = True
		for myfile in local_files_toexecute:
			if step_ok : step_ok = subprocess.call(['{}/make_local_files_executable.sh'.format(Path_bash), '{}/{}'.format(Path_bash,myfile)])
		if step_ok:
			txt_OK()
			return True
		else:
			txt_NOK("file {} is missing".format(myfile))
			return False
	def sshkey_activation():		
		txt_Proceed("activation de la clé ssh via clef cryptée")
		stdexit = subprocess.call(['{}/start_ssh.sh'.format(Path_bash), '-e'])
		if not stdexit :
			txt_OK()
			return True
		else:
			txt_NOK()
			return False
	def check_internet_connect():
		txt_Proceed("Check Internet access")
		if not subprocess.call('{}/check_internet.sh'.format(Path_bash)): 
			txt_OK()
			return True
		else:
			txt_NOK("internet connexion required")
			return False
	def pull_git():
		txt_Proceed("Git pull")
		stdexit = subprocess.call(['{}/git_pull.sh'.format(Path_bash)])
		if not stdexit :
			txt_OK()
			return True
		else:
			txt_NOK()
			return False
		return True	
	step_ok = True
	
	
	Step_OK : Step_OK= make_local_files_executable()
	if Step_OK : Step_OK= sshkey_activation()
	if Step_OK and not (options['no_down'] and options['no_update']): Step_OK= check_internet_connect()
	if Step_OK and not options['no_update']: Step_OK= pull_git()
	return Step_OK
	
def files_transfert(**options):		
	def copy_sav():
		txt_Proceed('local copy of files')
		step_ok = True
		
		for funct in List_to_transfer:
			for myfile in local_files_totransfer:
				if funct in myfile['functions']:
					if step_ok: step_ok = subprocess.run(['sudo', 'cp', '{}/{}.sav'.format(Path_files,myfile['file']), '{}/{}'.format(Path_files,myfile['file'])])
					if step_ok: step_ok = subprocess.run(['sudo', 'chmod', '777', '{}/{}'.format(Path_files,myfile['file'])])
					if not step_ok: 
						txt_NOK(myfile['file'])
						return False
		txt_OK()
		return True
	def hostapd_conf():
		txt_Proceed("update hostapd config")
		hostapd_conf_add=[	"ssid={}".format(str.capitalize(Target['os'].hostname)),
							"wpa_passphrase=@{}4884{}".format(str.capitalize(Target['user'].username),str.capitalize(Target['os'].hostname))] 
		if add_lines(hostapd_conf_add, "{}/hostapd.conf".format(Path_files)):
			txt_OK()
		else:
			txt_NOK
			return False
		
		txt_Proceed("update hostapd.accept list")
		netcards_list = [auth_host.networkcard.mac_addr for auth_host in Host_Network.objects.using('system').filter(routed_by=Target['bridge'], network__system=Target['system'])]
		if add_lines(netcards_list, "{}/hostapd.accept".format(Path_files)):
			txt_OK()
		else:
			txt_NOK
			return False
			
		txt_Proceed("update interfaces file")
		
		lines_interface = [	'        address {}'.format(Target['host_network'].IPv4),
							'        netmask {}'.format(Target['host_network'].network.netmask),
							'        network {}'.format(Target['host_network'].network.network),
							'        broadcast {}'.format(Target['host_network'].network.broadcast)]
		if add_lines(lines_interface, "{}/interfaces".format(Path_files)):
			txt_OK()
			return True
		else:
			txt_NOK
			return False
	def files_transfer():
		txt_Proceed("files transfer")
		for funct in List_to_transfer:
			for myfile in local_files_totransfer:
				if funct in myfile['functions']:
					try:
						if myfile['owner_change']=='file' : 
							stdin, stdout, stderr = Target['ssh'].Client.exec_command("sudo chown -R {} {}/{}".format(Target['user'].username,myfile['target'],myfile['file']))
						elif myfile['owner_change']=='dir': 
							stdin, stdout, stderr = Target['ssh'].Client.exec_command("sudo chown -R {} {}".format(Target['user'].username,myfile['target']))
						stdout.channel.recv_exit_status()
						print(myfile['file'])
						Target['ssh'].ftp_Client.put('{}/{}'.format(Path_files,myfile['file']),'{}/{}'.format(myfile['target'],myfile['file']))
						print(myfile['file'])
					except:
						txt_NOK(myfile['file'])
						return False
		txt_OK()
		return True
	def copy_remove():
		txt_Proceed('remove copy')
		
		for funct in List_to_transfer:
			for myfile in local_files_totransfer:
				if funct in myfile['functions']:
					subprocess.run(['sudo', 'rm', '{}/{}'.format(Path_files,myfile)])
		txt_OK()
		return True
	
	List_to_transfer=['system']
	if Target['bridge']: List_to_transfer.append('bridge')
	
	Step_OK=True
	if Step_OK : Step_OK = copy_sav()
	time.sleep(1)
	if Step_OK : Step_OK = hostapd_conf()
	if Step_OK : Step_OK = files_transfer()
	#if Step_OK : Step_OK = copy_remove()
	return Step_OK
	
def git_push(**options):
	
	return True

def ssh_configuration(**options):
	def ssh_passwd():
		txt_Proceed("génération du mot de passe")
		stdin, stdout, stderr = Target['ssh'].Client.exec_command("echo $(openssl rand -base64 32)")
		stdout.channel.recv_exit_status()
		if stderr.readlines():
			txt_NOK()
			return False
		else:
			Target["ssh_passwd"] = stdout.readlines()[0][:-1]
			txt_OK()
			return True
		
	def ssh_keygen():
		txt_Proceed("génération de la clé ssh")
		command = 'printf "\n'
		#On commence par regarder si le fichier ".ssh/id_rsa_exist"
		stdin, stdout, stderr = Target['ssh'].Client.exec_command("if [ -f .ssh/id_rsa ]; then echo 1; else echo 0; fi")
		stdout.channel.recv_exit_status()
		if stdout.readlines()[0]=="1\n": command += 'y\n'
		command += '{0}\n{0}\n" | ssh-keygen'.format(Target["ssh_passwd"])
		stdin, stdout, stderr = Target['ssh'].Client.exec_command(command)
		stdout.channel.recv_exit_status()
		if stdout.readlines()[-1]=="+----[SHA256]-----+\n" :
			txt_OK()
			stdin, stdout, stderr = Target['ssh'].Client.exec_command("echo $(cat .ssh/id_rsa.pub)")
			stdout.channel.recv_exit_status()
			Target["ssh_pub"] = stdout.readlines()[0][-1]
			return True
		else:
			txt_NOK()
			return False
			
	def ssh_autorized():
		txt_Proceed("ssh_keys authorized update")
		stdin, stdout, stderr = Target['ssh'].Client.exec_command("touch .ssh/authorized_keys")
		stdout.channel.recv_exit_status()
		try:
			Target['ssh'].ftp_Client.put('.ssh/id_rsa.pub','.ssh/authorized_keys')
			txt_OK()
			return True
		except:
			txt_NOK()
			return False
		
	def ssh_management():
		txt_Proceed("Management du ssh")
		txt_Todo()
		return True
			
	Step_OK=True
	if Step_OK : Step_OK = ssh_passwd()
	if Step_OK : Step_OK = ssh_keygen()
	if Step_OK : Step_OK = ssh_autorized()
	if Step_OK : Step_OK = ssh_management()
	
	return Step_OK

def net_downloads(**options):
	def run_check(txt_proceed,command,timeout, software=False):
		txt_Proceed(txt_proceed)
		stdin, stdout, stderr = Target['ssh'].Client.exec_command(command)
		cnt=0
		while True:
			if stdout.channel.exit_status == 0:
				if software:
					soft = Software.objects.using('system').get_or_create(desi=software[0], installer=software[1], package=software[2])
					img_soft = OS_Software.objects.using('system').get_or_create(software=soft[0], os=Target['os'])
				txt_OK()
				return True
			elif stdout.channel.exit_status > 0:
				txt_NOK()
				return False
			if cnt >= timeout:
				if Confirm ('\n Programmed Timeout of {}s reached would you like to continue'):
					cnt=0
				else:
					txt_NOK()
					return False
			cnt+=1
			time.sleep(1)
			
	Step_OK=True

	if Step_OK: Step_OK = run_check("Packages Updates",'echo "O" | sudo apt-get update', 5)
	for pack,timeout in apt_packages.items():
		if Step_OK: Step_OK = run_check("Install {}".format(pack),'echo "O" | sudo apt-get -y install {}'.format(pack), timeout, software=(pack,"apt",True))
	
	for pack,timeout in pip_packages.items():
		if Step_OK: Step_OK = run_check("Install {}".format(pack),'echo "O" | pip3 install {}'.format(pack), timeout, software=(pack,"pip",True))
	
	if Step_OK: Step_OK = run_check("Change python-alternative",'sudo update-alternatives --install /usr/bin/python python /usr/bin/python3 1', 30)
	
	if Target['bridge']:
		for pack,timeout in apt_packages_bridge.items():
			if Step_OK: Step_OK = run_check("Install {}".format(pack),'echo "O" | sudo apt-get -y install {}'.format(pack), timeout, software=(pack,"apt",True))
	
			
	return Step_OK
	'''
	#subprocess.call(['{}/mymake.sh'.format(Path_bash)])
	stdin, stdout, stderr = ssh.Client.exec_command('echo "O" | sudo apt-get install git jq; touch ssh_done')
	for i in range(20):
		print(i, stdout.channel.exit_status)
		time.sleep(1)
	stdout.channel.recv_exit_status()
			
	stdin, stdout, sterr = ssh.Client.exec_command('sudo rm ssh_done & echo "OK"')
	print('nok')
	stdout.channel.recv_exit_status()
	for line in sterr.readlines():
		print(line)
	for line in stdout.readlines():
		print(line)
	'''
	
def get_target(**options):
	class SSH_Connection():
		def __init__(self):
			self.Client = paramiko.SSHClient()
			self.Client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			
			try:
				self.Client.connect(hostname = Target['ipv4'],
									port = 22, 
									username = Target['user'].username, 
									password = Target['password'], 
									look_for_keys = False, 
									allow_agent = False,
									timeout = 3)
				self.ftp_Client=self.Client.open_sftp()
				self.ok = True
			except: self.ok = False
	def check_os_exist():
		txt_Request("Please inform target's hostname")
		hostname = input()
		txt_Proceed("check target exist")
		try:
			os = OS.objects.using('system').get(hostname = hostname)
			Target["os"]=os
			txt_OK()
			return True
		except:
			txt_NOK("missing target in database")
			return False
	def confirm_target_info():
		# Software
		txt_Proceed("Check")
		txt_title("\tos")
		for key, value in Target["os"].__dict__.items():
			txt_Dict(key, value)	
		return Confirm("Are those informations OK")		
	def check_host_activ():
		txt_Proceed("Check host activ")
		hosts=Host.objects.using('system').filter(os = Target["os"])
		if len(hosts)==0: 
			txt_NOK("There is no CPU configured with this os")
			return False
		else:
			host_activ=Host.objects.using('system').filter(os = Target["os"], activ=True)
			if len(host_activ)==0: 
				txt_NOK("There is no activ Host configured with this os")
				return False
			elif len(host_activ)>1:
				txt_NOK("There is several Hosts configured with this os")
				return False
			else:
				txt_OK()
				Target["host"] = host_activ[0]
				Target["cpu"] = host_activ[0].cpu
		
		txt_Proceed("Check")
		txt_title("\tCPU")
		for key, value in Target["cpu"].__dict__.items():
			txt_Dict(key, value)
		
		
		txt_Proceed("Check activ system associated")
		host_net = Host_Network.objects.using('system').filter(networkcard__cpu=Target["cpu"])
		if len(host_net)==0: 
			txt_Warning("There is no network connection configured")
		else:	
			host_net_activ = Host_Network.objects.using('system').filter(networkcard__cpu=Target["cpu"], network__system__activ=True)
			if len(host_net_activ)==0:
				txt_NOK("No activ system linked to this CPU")
				return False
			elif len(host_net_activ)>1:
				txt_NOK("several activ systems linked to this CPU")
				return False
			else:
				txt_OK()
				Target['system']=host_net_activ[0].network.system 
		
		txt_Proceed("Check")
		txt_title("\tCPU's Network Cards")
		networkcards=NetworkCard.objects.using('system').filter(cpu=Target["cpu"])
		if len(networkcards)==0: 
			txt_NOK("There is no Card attributed to this CPU's")
			return False
		
		host_network_temp=None	
		for netcard in networkcards:
			txt_subtitle1("netcard {}".format(netcard.detail))
			for key, value in netcard.__dict__.items():
				txt_Dict(key, value)
			
			bridged_hosts = Host_Network.objects.using('system').filter(routed_by=netcard, network__system=Target['system'])
			if len(bridged_hosts)>0: 	
				txt_Dict("Bridge","\033[92mYES\033[m")
				Target['bridge']=netcard
			else: 
				txt_Dict("Bridge","NO")
			
			if not Target["bridge"]:
				txt_subtitle2("activ network associated")
				host_net = Host_Network.objects.using('system').filter(networkcard=netcard)
				if len(host_net)==0: 
					txt_Warning("There is no network connection configured")
				else:	
					host_net_activ = Host_Network.objects.using('system').filter(networkcard=netcard, network__system__activ=True)
					if len(host_net_activ)==0: txt_Warning("Missing connection to activ System")
					elif len(host_net_activ)>1 : txt_Warning("Strange, you shouldn't get several activ connection, make sure ther not several system activ")
					else:
						host_net_activ=host_net_activ[0]
						txt_Dict("System",host_net_activ.network.system.desi)
						txt_Dict("Network",host_net_activ.network.desi)
						host_network_temp=host_net_activ
						for key, value in host_net_activ.__dict__.items(): txt_Dict(key, value)
			else:
				for b_host in bridged_hosts:
					txt_Dict("\t{}".format(b_host.networkcard.cpu.desi), b_host.IPv4)
						
			
					
		if	Confirm("Are those informations OK"):	
			Target['host_network'] = host_network_temp
			return True
		return False 
	def select_CPU():
		txt_Proceed("Select CPU which is used for configuration")
		txt_title("CPU")
		cpu_host=None
		if Confirm("is the os currently hosted by final host : {}".format(Target['cpu'].desi)):
			Target['cur_cpu'] = Target['cpu']
			return True
		else:
			txt = "Inform CPU's designation"
			while True:
				txt_Request(txt)
				cpu = input()
				if cpu=="e": return False
				if len(CPU.objects.using('system').filter(desi=cpu))==1: 
					Target['cur_cpu'] = CPU.objects.using('system').get(desi=cpu)
					return True
				else:
					txt = "Inform Valid designation or \"e\" to exit"
		return False
	def select_ip():
		host_net = Host_Network.objects.using('system').filter(networkcard__cpu=Target['cur_cpu'])
		if len(host_net)==0: 
			txt_NOK("There is no network connection configured")
			return False
		else:
			host_net_activ = Host_Network.objects.using('system').filter(networkcard__cpu=Target['cur_cpu'], network__system__activ=True)
			if len(host_net_activ)==0: 
				txt_NOK("There is no network connection configured on activ system")
				return False
			else:
				select_List = [ "{}\t-\t{}\t-\t{}".format(host_net.networkcard.type,host_net.IPv4,host_net.network.system) for host_net in host_net_activ]
				try: 
					Target["cur_host_net"] = host_net_activ[Select(select_List, "IP")]
					Target["ipv4"] = Target["cur_host_net"].IPv4
				except: return False		
	def select_User():
		txt_Proceed("Select")
		txt_title("\tUser")
		usr_imgs=OS_User.objects.using('system').filter(os = Target["os"])
		if len(usr_imgs)==0: 
			txt_NOK("There is no user attributed to this os")
			return False
		else:
			select_List = [ usr_img.user.username for usr_img in usr_imgs]
			try: 
				Target["user_img"] = usr_imgs[Select(select_List, "User")]
				Target["user"] = Target["user_img"].user
				Target["password"] =  Target["user_img"].password
				return True
			except: return False
	def ping_host():
		if Target['method']==0:
			while True:
				txt_Request("IP addres of the connected Host (\"e\" to exit)")
				inp = input()
				if inp=="e": return False
				txt_Proceed("Ping check")
				time.sleep(0.1)
				if subprocess.call(['{}/ping_check.sh'.format(Path_bash), '{}'.format(inp)])==1:
					txt_NOK("Host not connected")
				else:
					Target['ipv4']=inp
					txt_OK()
					return True
		else:
			txt_Proceed("Ping check")
			time.sleep(0.1)
			if subprocess.call(['{}/ping_check.sh'.format(Path_bash), '{}'.format(Target['cur_host_net'].IPv4)])==1:
				txt_NOK("Host not connected")
			else: txt_OK()
			return True				
	def connection_try():		
		txt_Proceed("Ssh connection check")
		ssh = SSH_Connection()
		if ssh.ok:
			Target['ssh']=ssh
			txt_OK()
			return True
		else:
			txt_NOK("")
			return False
				
	Step_OK= check_os_exist()
	if Step_OK : Step_OK= confirm_target_info()
	if Step_OK : Step_OK= check_host_activ()
	if Step_OK and Target['method']!=0: Step_OK= select_CPU()
	if Step_OK and Target['method']!=0 : Step_OK= select_ip()
	if Step_OK : Step_OK= select_User()
	if Step_OK : Step_OK= ping_host()
	if Step_OK : Step_OK= connection_try()
	return Step_OK

def select_config_mode(**options):
	txt_Proceed("Select configuration method")
	txt_title("Config")
	txt_Present("0 - External - systematic - to prefer")
	sys.stdout.write(" This CPU is connected to CPU's Host thanks direct RJ45 wire \n both are connected to internet through Wifi\n to be preferred in case there is Firewall on the active system (block internet access)\n")
	txt_Present("1 - OnBoard - if no restriction on system")
	sys.stdout.write("CPU defined in config database will be directly used \n")
	select_List = ["External", "OnBoard"]
	Target["method"]=Select(select_List, "Method")
	if Target["method"]=="exit":return False
	return True	

def add_lines(lines,myfile):
	step_ok = True
	for line in lines:
		if step_ok: step_ok = subprocess.call(['{}/add_line.sh'.format(Path_bash),myfile, line])
	return step_ok
