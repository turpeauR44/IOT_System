#! /usr/bin/python3
#	Import des librairies
	#	Standard
import time
import sys
import os
import psutil
from system.management.functions.utils import date_now

	#	Django
from django.core.management.base import BaseCommand, CommandError

	#	Projet
from IOT.processus import *
import IOT.log as application_log

from software.models import OS as OS_M
from hardware.models import CPU as CPU_M, NetworkCard as Net_M
from host.models import Host as Host_M, Guest as Guest_M, Guest_Processus as Guest_Processus_M
			
class Command(BaseCommand):
	help = 'Commande de lancement de la boucle run de host'
	
	def add_arguments(self, parser):
		parser.add_argument('-U', dest='user', type=str)
		parser.add_argument('-d', dest='debug', action='store_true')
	def handle(self, *args, **options):
			# Recuperation des arguments systeme
		user = options['user']
		Debug = options['debug']
		application_log.init_appli_log_path(user)
		application_log.write("", timestamp=False)
		application_log.write("Lancement application host")
		application_log.init_debug_value(Debug)
			# Creation de l'objet Host
		host = Host()
		while True:
			for guest in host.guests:
				for proc in guest.processus:
					try: 
						proc_requested=((date_now() - proc.obj.start_at).seconds > proc.obj.period)
					except:
						proc_requested=True
					if proc_requested:
						if Debug: print("boucle: \t guest : {}, \t processus : {}".format(guest.obj.desi, proc.obj.processus.type))
						try:
							proc.obj.start_at = date_now()
							proc.inst.Loop()
							proc.obj.save()
						except:
							if Debug: print("failed to perform processus")
					
			time.sleep(1)
			
		
class Host():
	def __init__(self):
		# L'hote est défini à partir du software:
		self.ok=exist_os()
		if self.ok : local_os = OS_M.objects.using('system').get(hostname=os.uname()[1])
		#L'hote est aussi défini à partir de sa CPU. si on ne connait pas sa référence de la base dans le système, on peut retrouver ses cartes réseaux et don le déduire
		if self.ok : self.ok, cpu = exist_cpu()
		if self.ok : self.ok, self.obj = exist_host(local_os, cpu)
		if self.ok : self.guests = [Guest(guest) for guest in Guest_M.objects.using('system').filter(host=self.obj).order_by('id')]

class Guest():
	def __init__(self,guest):
		self.obj = guest
		self.processus = [Processus(guest_proc) for guest_proc in Guest_Processus_M.objects.filter(guest=guest).order_by('id')]
		
class Processus():
	Librairy={'pline_status':PLine_Status,'hub':Hub,'scrut':Scrut}
	def __init__(self,guest_proc):
		self.obj = guest_proc
		self.inst = Processus.Librairy[self.obj.processus.type].Processus(guest_proc)


def exist_os():
	if len(OS_M.objects.using('system').filter(hostname=os.uname()[1]))==1: 
		application_log.write("local_os found in database", timestamp=False)
		return True
	else:
		application_log.write("Failed to find local_os in database", timestamp=False)
		return False
def exist_cpu():
	addrs_mac = []
	for addr in psutil.net_if_addrs().values():
		 for infos in addr:
			 if infos.family._name_ == "AF_PACKET" and infos.address != "00:00:00:00:00:00": addrs_mac.append(infos.address)
	cpu = None
	for addr_mac in addrs_mac:
		new_cpu = Net_M.objects.using('system').filter(mac_addr=addr_mac)[0].cpu
		if cpu and new_cpu != cpu : 
			application_log.write("Network mac address issue in database", timestamp=False)
			return False
		else: cpu = new_cpu
	if cpu :
		application_log.write("cpu found in database", timestamp=False)
		return True, cpu
	else:
		application_log.write("missing cpu in database", timestamp=False)
		return False, None
def exist_host(local_os,cpu):
	try:
		application_log.write("corresponding host found in database", timestamp=False)
		host = Host_M.objects.using('system').get(os=local_os, cpu=cpu)
		return True, host
	except:
		application_log.write("missing host in database", timestamp=False)
		return False
		
'''

		

'''
