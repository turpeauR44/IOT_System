from django.db import models
from django.utils.translation import gettext_lazy as trad
from django.contrib.auth.models import User
from wshop.models import Equipment
'''-------------------------	Système		---------------------------'''
'''-------------------------	Network		---------------------------'''
class System (models.Model):
	# Le système est en quelque sorte l'environnement dans lequel vous évolué
	# On pourra ainsi spécifier des addresse IP spécifique à cet environnement, des réseaux
	class Meta:
		db_table			='TAB_SYSTEMS'
		verbose_name		='System'
		verbose_name_plural = 'Systems'
		admin_site_details	= {'index':0, 'parent':'Network'}
		
	class Environnement(models.TextChoices):
		DEV 		= 'dev', trad('Développement')
		PROD 		= 'prod', trad('Production')
		TEST		= 'test', trad('Test')
	desi 		= models.CharField(max_length=16, unique=True)
	environnement=models.CharField(max_length=4, choices = Environnement.choices, default = Environnement.DEV)
	activ		= models.BooleanField(default=False)
	
	def __str__(self):
		return self.desi
class Network (models.Model):
	# Le Network est le reseau dans le cas ou plusieurs reseau composent votre système
	# 
	class Meta:
		db_table			='TAB_NETWORKS'
		verbose_name 		= "Réseau"
		verbose_name_plural = "Networks"
		admin_site_details= {'index':0}
		constraints = [
            models.UniqueConstraint(fields=['desi', 'system'], name = 'Réseau unique')
            ]
	class Type(models.TextChoices):
		ETHERNET 		= 'eth', trad('réseau ethernet')
		WIFI  			= 'wlan', trad('wifi')
	desi 		= models.CharField('designation',max_length=16)
	type 		= models.CharField('type',max_length=4, choices = Type.choices, default = Type.ETHERNET)
	system 		= models.ForeignKey('System', null=True, on_delete=models.CASCADE)
	network 	= models.GenericIPAddressField(default="255.255.255.0")
	netmask 	= models.GenericIPAddressField(default="255.255.255.0")
	broadcast 	= models.GenericIPAddressField(default="255.255.255.0")
	
	def __str__(self):
		return "{} - {}".format(self.system, self.desi)

'''-------------------------	Hardware	---------------------------'''
class CPU (models.Model):
	#Micro-ordinateur (Hardware)
	#
	class Meta:
		db_table			='TAB_CPUS'
		verbose_name 		= "micro-ordinateur"
		verbose_name_plural = "Processing Units"
		admin_site_details 	= {'index':1, 'parent':'Host'}
	class Model(models.TextChoices):
		PI4_8Go 		= 'pi4_8go', trad('Raspberry Pi 4 - 8Go')
		PI4_4Go 		= 'pi4_4go', trad('Raspberry Pi 4 - 4Go')
		PI4_2Go 		= 'pi4_2go', trad('Raspberry Pi 4 - 2Go')
		PI3_1Go 		= 'pi3_1go', trad('Raspberry Pi 3 model B+ - 1Go')
		PI0_512Mo 		= 'pi0_512mo', trad('Raspberry Pi 0 - 512Mo')
	desi		= models.CharField('designation', max_length=12, default="CROWNXXXX")
	model 		= models.CharField('modèle', max_length=12, choices = Model.choices, default = Model.PI4_4Go)
	
	def __str__(self):
		return self.desi		
class NetworkCard (models.Model):
	class Meta:
		db_table			='TAB_NETWORKCARDS'
		verbose_name 		= "Carte réseau"
		verbose_name_plural = "Cartes réseau"
		admin_site_details 	= {'index':1, 'parent':'CPU'}
	class Type(models.TextChoices):
		ETHERNET 		= 'eth', trad('réseau ethernet')
		WIFI  			= 'wlan', trad('wifi')
	cpu 		= models.ForeignKey('CPU', on_delete=models.CASCADE)
	mac_addr 	= models.CharField('adresse mac', max_length=17,unique=True, default="00:00:00:00:00:00") #Ajouter ici un validator
	type 		= models.CharField('type', max_length=4, choices = Type.choices, default = Type.ETHERNET)
	detail		= models.CharField('détails', max_length=8, default="eth0")
	
	def __str__(self):
		return "{} - {} - {}".format(self.cpu.desi, self.type , self.detail)
class Host_Network (models.Model):
	class Meta:
		db_table			='TAB_HOST_NETWORKS'
		verbose_name 		= "adresse réseau"
		verbose_name_plural = "Adresses réseau"
		admin_site_details 	= {'index':2, 'parent':'Network'}
	networkcard	= models.ForeignKey(NetworkCard, on_delete=models.CASCADE)
	network 	= models.ForeignKey('Network', on_delete=models.CASCADE)
	IPv4 		= models.GenericIPAddressField(default="0.0.0.0")
	routed_by	= models.ForeignKey(to=NetworkCard, on_delete=models.CASCADE, null=True, blank=True, related_name="router")
	
	def __str__(self):
		return "{} - {}".format(self.network.system, self.network.desi)

'''-------------------------	Software	---------------------------'''
class OS(models.Model):
	#L'image comme son nom l'indique est la configuration portée par la carte SD
	#
	class Meta:
		db_table			='TAB_SDCARDS'
		verbose_name 		= "OS"
		verbose_name_plural = "Operating System"
		admin_site_details 	= {'index':2, 'parent':'Host'}
	class Type(models.TextChoices):
		WIN 		= 'win', trad('Windows')
		FULL 		= 'full', trad('Raspbian Buster')
		LITE  		= 'lite', trad('Raspbian Buster lite')
	id 			= models.IntegerField(default=0, primary_key=True)
	hostname 	= models.CharField(max_length=16, unique=True)
	ssh_pub		= models.CharField(max_length=512, null=True, blank=True)
	type 		= models.CharField(max_length=12, choices = Type.choices, default = Type.FULL, verbose_name="Operating System")
	
	softwares 	= models.ManyToManyField('Software',through='OS_Software')
	users 		= models.ManyToManyField(User,through='OS_User') 
	
	def __str__(self):
		return "{} - {}".format(self.id, self.hostname) 
class OS_User(models.Model):
	class Meta:
		db_table			='TAB_USER_OS'
		verbose_name 		= "utilisateur OS"
		verbose_name_plural = "Utilisateurs OS"
		#admin_site_details 	= {'index':1, 'parent':'OS'}
	os 			= models.ForeignKey('OS', on_delete=models.CASCADE)
	user 		= models.ForeignKey(User, on_delete=models.CASCADE)
	password 	= models.CharField(max_length=512, null=True, blank = True)
class Software(models.Model):
	class Meta:
		db_table			='TAB_SOFTWARES'
		verbose_name 		= "Logiciel"
		verbose_name_plural = "Softwares"
		admin_site_details 	= {'index':2, 'parent':'OS'}
	class Installer(models.TextChoices):
		UNDEFINED	= 'undefined', trad('non-défini')
		APT 		= 'apt', trad('apt')
		PIP 		= 'pip', trad('pip')
	desi 		= models.CharField(max_length=12, unique = True)
	desc 		= models.CharField(max_length=128)
	installer 	= models.CharField(max_length=24, choices = Installer.choices, default = Installer.UNDEFINED)
	package		= models.BooleanField(default=False)
	def __str__(self):
		return self.desi
class OS_Software(models.Model):
	class Meta:
		db_table			='TAB_OS_SOFTWARES'
		verbose_name 		= "Liaison Logiciel OS"
		verbose_name_plural = "Liaison Logiciels OS"
		admin_site_details 	= {'index':2, 'parent':'OS'}
	#configFile 	= models.FileField(null=True, blank=True)
	software 	= models.ForeignKey('Software', on_delete=models.CASCADE)
	os 	  		= models.ForeignKey('OS', on_delete=models.CASCADE)

'''-------------------------	Hôte		---------------------------'''
class Host (models.Model):
	# L'hôte est une combinaison 
	class Meta:
		db_table			= 'TAB_HOSTS'
		verbose_name 		= "Hôte"
		verbose_name_plural = "Hotes"
		admin_site_details= {'index':1}
	os 		= models.ForeignKey(OS, on_delete=models.CASCADE)
	cpu 	= models.ForeignKey(CPU, on_delete=models.CASCADE)
	activ	= models.BooleanField(default=False)

	def __str__(self):
		return "{} - {} - {} - {}".format(self.os.id, self.os.hostname, self.cpu.model, self.cpu.desi)
class Guest (models.Model):
	class Meta:
		db_table			='TAB_GUESTS'
		verbose_name 		= "Guest"
		verbose_name_plural = "Guests"
		admin_site_details 	= {'index':3, 'parent':'Host'}
	class Type(models.TextChoices):
		PRODLINE 			= 'p', trad('Ligne de production')
		EQUIPMENT  			= 'e', trad('Equipement')
		WSHOP 				= 'w', trad('Atelier')
		SERVER 				= 's', trad('Serveur')
	host 		= models.ForeignKey('Host', on_delete=models.CASCADE)
	desi 		= models.CharField(max_length=16, unique=True)
	type 		= models.CharField(max_length=4, choices = Type.choices, default = Type.EQUIPMENT)
	
	def __str__(self):
		return '{} - {}'.format(self.host.cpu, self.Type._value2label_map_[self.type])
class Guest_Processus (models.Model):
	class Meta:
		db_table			='TAB_GUEST_PROCESSUS'
		verbose_name 		= "Guest Processus"
		verbose_name_plural = "Guest_Processus"
		#admin_site_details 	= {'index':1, 'parent':'Guest'}
	guest 		= models.ForeignKey('Guest', on_delete =models.CASCADE)
	processus 	= models.ForeignKey('Processus', on_delete =models.CASCADE)
	activ 		= models.BooleanField(default=False)
	start_at 	= models.DateTimeField(auto_now_add=True)
	period 		= models.IntegerField(default=5)
	
	def __str__(self):
		return "{} - {}".format(self.processus.type, self.guest.desi)
class Processus (models.Model):
	class Meta:
		db_table			='TAB_PROCESSUS'
		verbose_name 		= "Processus"
		verbose_name_plural = "Processus"
		admin_site_details 	= {'index':1, 'parent':'Guest'}
	desi 		= models.CharField(max_length=16, unique=True)
	details 	= models.JSONField(null=True, blank=True)
	def __str__(self):
		return self.desi
class Database (models.Model):
	class Meta:
		db_table			='TAB_DATABASES'
		verbose_name 		= "Database système"
		verbose_name_plural = "Databases système"
	host 		= models.ForeignKey(Host, on_delete=models.CASCADE)
	user 		= models.CharField(max_length=32, default="postgres")
	password 	= models.CharField(max_length=32)

'''-------------------------	InOutput	---------------------------'''
class Controller (models.Model):
	class Meta:
		db_table='TAB_CONTROLLERS'
		verbose_name = "Controller"
		verbose_name_plural = "Controllers"
	class Board(models.TextChoices):
		UNO 			= 'uno', trad('Arduino uno')
		NANO  			= 'nano', trad('Arduino nano')
		UNO_GEN  		= 'uno_gen', trad('Generic uno')
		NANO_GEN  		= 'nano_gen', trad('Generic nano')
		admin_site_details 	= {'index':2}
	
	guest = models.ForeignKey(Guest, on_delete =models.CASCADE)
	desi = models.CharField('desigation', max_length=16, unique = True)
	board = models.CharField(max_length=16, choices = Board.choices, default = Board.NANO)
	baud = models.IntegerField(default = 9600)
	serial = models.CharField(max_length=32, default = "None")
	period = models.IntegerField(default = 15000)
	transfer_dur = models.IntegerField(default = 10)
	nb_pulsmax = models.IntegerField(default = 100)
	
	def __str__(self):
		return "{} - {}".format(self.desi, self.guest)		
class IO (models.Model):
	class Meta:
		db_table='TAB_IOS'
		verbose_name = "Signal IO"
		verbose_name_plural = "Signaux (IO)"
		constraints = [
            models.UniqueConstraint(fields=['controller', 'code'], name = 'unique io_code par controller')
            ]
		admin_site_details 	= {'index':1, 'parent':'Controller'}
	class Put(models.TextChoices):
		IN = 'in'
		OUT='out'
		NOT='not'
	class Type(models.TextChoices):
		DIGITAL = 'digital'
		ANALOG = 'analog'
		NOT='not'
	controller 	= models.ForeignKey(Controller, on_delete=models.CASCADE)
	equipment 	= models.ForeignKey(Equipment, null = True, on_delete=models.CASCADE)
	desi 		= models.CharField('designation', max_length=254)
	put 		= models.CharField('signal', max_length=16,choices=Put.choices, default=Put.IN)
	type		= models.CharField('type', max_length=16,choices=Type.choices, default=Type.DIGITAL)
	code 		= models.CharField(max_length=16)
	pin 		= models.CharField(max_length=16)
	
	def __str__(self):
		return "{} - {} - {} - {}".format(self.equipment, self.controller, self.code, self.desi)
class Digital_IO (models.Model):
	class Meta:
		db_table='TAB_DIGITAL_I0S'
		verbose_name = "signaux digitaux"
		admin_site_details 	= {'index':1, 'parent':'IO'}
	initial 	= models.IntegerField(default = 0)
	Period_Min 	= models.IntegerField(default = 100)
	Pulse_Min  	= models.IntegerField(default = 100)
	Period_Max 	= models.IntegerField(default = 100)
	Pulse_Max  	= models.IntegerField(default = 100)
	io = models.ForeignKey('IO', on_delete=models.CASCADE)
class Analog_IO (models.Model):
	class Meta:
		db_table='TAB_ANALOG_I0S'
		verbose_name = "signaux analogiques"
		admin_site_details 	= {'index':2, 'parent':'IO'}
	min = models.IntegerField(default = 0)
	val_min = models.IntegerField(default = 0)
	max = models.IntegerField(default = 0)
	val_max = models.IntegerField(default = 0)
	io = models.ForeignKey('IO', on_delete=models.CASCADE)
class Log_Type(models.Model):
	class Meta:
		db_table='TAB_LOG_TYPES'
		verbose_name = "Type Log"
		verbose_name_plural = "Log Type"
		constraints = [
            models.UniqueConstraint(fields=['type', 'subtype', 'io_type'], name = 'unique type subtype et signal')
            ]
		admin_site_details 	= {'index':2, 'parent':'Controller'}
	type 		= models.CharField(max_length=16)
	subtype 	= models.CharField(max_length=16)
	io_type 	= models.CharField(max_length=16,choices=IO.Type.choices)
	io_put  	= models.CharField(max_length=16,choices=IO.Put.choices)
	
	def __str__(self):
		return "{} - {} - {} - {}".format(self.io_type, self.io_put, self.type, self.subtype)
		
	def get_logtypes_dict():
		Dict = {}
		for Type in IO.Type.choices:
			for Put in IO.Put.choices:
				TypePut = "{}{}".format(Type[0],Put[0])
				Dict[TypePut] = Log_Type.objects.using('system').filter(io_type= Type[0], io_put= Put[0]).order_by('id')
		return Dict
class Log(models.Model):
	class Meta:
		db_table='TAB_LOGS'
		verbose_name = "Log"
		verbose_name_plural = "Log"
	log_type 	= models.ForeignKey('Log_Type', on_delete=models.CASCADE)
	io			= models.ForeignKey('IO', on_delete=models.CASCADE)

