import host.models as HM
import psycopg2
from system.management.functions.utils import date_now, get_max

from IOT.log import write as log_write, return_Debug


class Processus():
	def __init__(self,obj):
		self.pline = obj.guest.desi[1:].upper()
		self.host = obj.guest.host
		log_write("Initialisation du processus Pline_Status" + self.pline)
		self.debug = return_Debug()
		
		self.controller= HM.Controller.objects.get(guest=obj.guest, desi="no_controller")
		book = HM.Book.objects.create(controller=self.controller, timestamp=date_now(), io_type='not', io_put='not')
		
		status_logtype = HM.Log_Type.objects.get(type="Status", subtype="Value", io_type='not', io_put='not')
		status_io = HM.IO.objects.get(desi="prodline_status", controller=self.controller, code="pl_st")
		self.status_log = HM.Log.objects.get_or_create(log_type=status_logtype, io=status_io)[0]
		log_value = HM.Log_Value.objects.get_or_create(log = self.status_log, value=0)
		log_book = HM.Log_Books.objects.create(first_book=book.id, last_book=book.id, log_value=log_value[0])
		
		status_speed_logtype = HM.Log_Type.objects.get(type="Speed", subtype="Value", io_type='not', io_put='not')
		status_speed_io = HM.IO.objects.get(desi="prodline_speed", controller=self.controller, code="pl_sp")
		self.status_speed_log = HM.Log.objects.get_or_create(log_type=status_speed_logtype, io=status_io)[0]
		log_value = HM.Log_Value.objects.get_or_create(log = self.status_speed_log, value=0)
		log_book = HM.Log_Books.objects.create(first_book=book.id, last_book=book.id, log_value=log_value[0])
		
		self.init_db_conn()
		
		self.speed 		= Speed(obj.processus.details['speed'],self.host)
		self.running	= Running(obj.processus.details['running'],self.host)
		self.producing	= Producing(obj.processus.details['producing'],self.host) 
		
	def init_db_conn(self):
		log_write("\tInitialisation connection base serveur", end=False, timestamp = False)			
		self.db_conn = psycopg2.connect(dbname='scrown', host='5.27.15.17', user='postgres', password='@Crown4884Postgres', port='5432')
		self.db_conn.autocommit=True
		self.cursor = self.db_conn.cursor()
		
	def Loop(self):
		self.status = 1
		self.status_speed = 0
		cond_update_speed=False
		cond_update_status=False
		
		
		for log in [self.speed, self.running, self.producing]:
			log.transform(log.get_value())
		
		if self.running.value:
			self.status = 2
			self.status_speed = self.speed.value
			if self.producing.value: self.status = 3
		
		duration = get_max([self.speed.duration, self.running.duration, self.producing.duration])
		last_book = HM.Book.objects.filter(controller=self.controller, io_type='not', io_put='not').latest('id')
		new_book = HM.Book.objects.create(controller=self.controller, timestamp=date_now(),duration = duration, io_type='not', io_put='not')
		
		last_status_log_book = HM.Log_Books.objects.get(last_book = last_book.id, log_value__log=self.status_log)
		if last_status_log_book.log_value.value != self.status:
			log_value = HM.Log_Value.objects.get_or_create(log = self.status_log, value= self.status)
			log_book = HM.Log_Books.objects.create(first_book=new_book.id, last_book=new_book.id, log_value=log_value[0])
			cond_update_status=True
		else:
			last_status_log_book.last_book=new_book.id
			last_status_log_book.save()
			
		last_status_speed_log_book = HM.Log_Books.objects.get(last_book = last_book.id, log_value__log=self.status_speed_log)
		if last_status_speed_log_book.log_value.value != self.status_speed:
			log_value = HM.Log_Value.objects.get_or_create(log = self.status_speed_log, value= self.status_speed)
			log_book = HM.Log_Books.objects.create(first_book=new_book.id, last_book=new_book.id, log_value=log_value[0])
			cond_update_speed=True
		else:
			last_status_speed_log_book.last_book=new_book.id
			last_status_speed_log_book.save()
			
		if cond_update_status or cond_update_speed:
			cond_db = True
			try:
				sql = ''' SELECT 1 '''
				self.cursor.execute(sql)
			except:
				if self.host.debug: print('reboot de la bdd')
				try:
					self.db_conn.close()
				except:
					pass
				try:
					self.init_db_conn()
					if self.host.debug: print('réinitialisation de la connexion OK')
				except:
					if self.host.debug: print('no way to reboot DB connexion')
					cond_db = False
			if cond_db:
				if cond_update_speed: self.update_speed()
				if cond_update_status: self.update_status()
				
				
		
	def update_speed(self):
		sql='''UPDATE "TAB_PRODLINES" SET cur_speed={} WHERE desi='{}' '''.format(self.status_speed, self.pline) 
		self.cursor.execute(sql)
	
	def update_status(self):
		sql='''UPDATE "TAB_PRODLINES" SET statut='{}' WHERE desi='{}' '''.format(self.status, self.pline) 
		self.cursor.execute(sql)

class Log():
	def __init__(self,details,processus_host):
		self.processus_host = processus_host
		self.IO_code = details['IO_code']
		self.controller = HM.Controller.objects.get(desi=details['controller_desi'])
		self.IO = HM.IO.objects.get(controller=self.controller, code=details['IO_code'])
		self.log_type=details['Log_type']
		self.log = HM.Log.objects.filter(log_type__type=self.log_type, io=self.IO)[0]
		self.host = self.controller.guest.host
		self.local = (self.host == processus_host)
		if not self.local:
			log_write("\tConfiguration de la base de donnée distante "+self.host.desi, timestamp = False)
			DB = HM.Database.objects.get(host=self.host)
			self.DB_user = DB.user
			self.DB_password = DB.password
			# Selection Network
			processus_networks = HM.Host_Network.objects.filter(host = processus_host)
			for net in processus_networks:
				host_network = HM.Host_Network.objects.filter(network_id=net.network_id, host = self.host)
				if len(host_network)>0:
					self.DB_addr = host_network[0].addr
					break
			self.DB_name = self.host.desi
			self.init_db_conn()
			
		self.value=False
		self.duration = 0
		
	def init_db_conn(self):	
		max_connection_attempt= 100
		log_write("\t\t\tInitialisation de la base de donnée distante "+self.host.desi , end = False, timestamp = False)
		self.db_conn_ok = False
		for attempt in range(max_connection_attempt):
			try: 	
				self.db_conn = psycopg2.connect(dbname=self.DB_name, host=self.DB_addr, user=self.DB_user, password=self.DB_password, port='5432', connect_timeout=1)
				self.db_conn.autocommit=True
				self.cursor = self.db_conn.cursor()
				self.db_conn_ok = True
				log_write("... ok" , timestamp = False)
				break
			except:
				log_write("#" , end = False, timestamp = False)
		#On doit récupérer les id des données requises dans la base target pour la suite: controller_id et log_id:
		sql = ''' SELECT id FROM "TAB_CONTROLLERS" WHERE desi='{}' '''.format(self.controller.desi)
		self.cursor.execute(sql)
		self.controller_id=self.cursor.fetchone()[0]
		sql = ''' SELECT TL.id FROM "TAB_LOGS" as TL 
					LEFT JOIN "TAB_LOG_TYPES" as TLT on TLT.id=TL.log_type_id
					LEFT JOIN "TAB_IOS" as TI on TI.id=TL.io_id
					WHERE TLT.type='{}' and TI.code='{}' and TI.controller_id={} '''.format(self.log_type, self.IO_code, self.controller_id)
		self.cursor.execute(sql)
		self.log_id=self.cursor.fetchone()[0]			
		
	def get_value(self):
		if self.processus_host.debug: print('Données locales ? :', self.local)
		if self.local:
			#On va chercher le dernier book du type de donnée requis
			try:
				last_book = HM.Book.objects.filter(controller=self.controller, io_type=self.IO.type, io_put=self.IO.put).latest('id')
				self.duration = last_book.duration
			except:
				last_book = False
			#On regarde si celui ci est lié au log qui nous intéresse:
			if last_book:
				try:
					last_log_book = HM.Log_Books.objects.get(last_book = last_book.id, log_value__log=self.log)
					return last_log_book.log_value.value
				except:
					return False
			return False
		else:
			cond_db=True
			try:
				sql = ''' SELECT 1 '''
				self.cursor.execute(sql)
			except:
				if self.processus_host.debug: print('reboot de la bdd')
				try:
					self.db_conn.close()
				except:
					pass
				try:
					self.init_db_conn()
					if self.processus_host.debug: print('réinitialisation de la connexion OK')
				except:
					if self.processus_host.debug: print('no way to reboot DB connexion')
					cond_db = False
					
			if cond_db:
				self.duration = 0
				sql = ''' SELECT id, duration FROM "TAB_BOOKS" WHERE controller_id={} and io_type='{}' and io_put='{}' ORDER BY id DESC LIMIT 1'''.format(self.controller_id,self.IO.type,self.IO.put) 
				self.cursor.execute(sql)
				res = self.cursor.fetchone()
				if res != None:
					book_id = res[0]
					self.duration = res[1]
					cond=True
					if self.processus_host.debug: print("dernier book identifié")
				else:
					cond=False
					if self.processus_host.debug: print("aucun book enregistré")
				if cond:
					sql = ''' SELECT TLV.value FROM "TAB_LOG_VALUES" as TLV 
								LEFT JOIN "TAB_LOG_BOOKS" as TLB on TLB.log_value_id=TLV.id
								WHERE TLV.log_id={} AND TLB.last_book={} '''.format(self.log_id, book_id)
					self.cursor.execute(sql)
					res = self.cursor.fetchone()
					if res != None:
						if self.processus_host.debug: print("log : {} \t value : {}".format(self.log_type, res[0]))
						return res[0]
					else:
						if self.processus_host.debug: print("pas de résultat")
						return False
				else:
					return False
			else:
				return False
		
class Speed(Log):
	def __init__(self,details,processus_host):
		Log.__init__(self,details,processus_host)
		self.str='speed'
		
	def transform(self,value):
		self.value = 0
		if self.log_type=="Period"and value: self.value = int(3600000/(int(value)+0.1))
		
class Running(Log):
	def __init__(self,details,processus_host):
		Log.__init__(self,details,processus_host)
		self.str='running'
		
	def transform(self,value):
		self.value = False
		if self.log_type=="Period" and value: self.value = True
		
class Producing(Log):
	def __init__(self,details,processus_host):
		Log.__init__(self,details,processus_host)
		self.str='producing'
		
	def transform(self,value):
		self.value = False
		if self.log_type=="Period" and value: self.value = True
