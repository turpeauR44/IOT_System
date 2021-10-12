from django.db import models
from django.utils.translation import gettext_lazy as trad

'''-------------------------	WShop		---------------------------'''
class WShop(models.Model):
	class Meta:
		db_table            ='TAB_WSHOPS'
		verbose_name        = "Atelier"
		verbose_name_plural = "Workshops"
		admin_site_details 	= {'index':1 }
	
	desi    = models.CharField('désignation', max_length=16, unique=True)
	desc    = models.CharField('description',max_length=2000, default='')
	
	def __str__(self):
		return self.desi

'''-------------------------	Collab		---------------------------'''
class Service(models.Model):
	class Meta:
		db_table            ='TAB_SERVICES'
		verbose_name        = "Service"
		verbose_name_plural = "Departments"
		admin_site_details 	= {'index':2}
	
	desi    = models.CharField('désignation', max_length=16, unique=True)
	desc    = models.CharField('description', max_length=200, default='')
	relates_to = models.ForeignKey(to='Service',null = True, on_delete=models.CASCADE)
	
	def __str__(self):
		return self.desi

class Function(models.Model):
	class Meta:
		db_table='TAB_FUNCTIONS'
		verbose_name = "Fonction"
		verbose_name_plural = "Fonctions"
		admin_site_details 	= {'index':1, 'parent':'Job'}
	
	desi    = models.CharField('désignation', max_length=16, unique=True)
	desc    = models.CharField('description', max_length=2000, default='')
		
	def __str__(self):
		return self.desc

class Job(models.Model):
	class Meta:
		db_table='TAB_JOBS'
		verbose_name = 'poste'
		verbose_name_plural= 'postes'
		admin_site_details 	= {'index':1, 'parent':'Service'}

	function    = models.ForeignKey(Function, on_delete=models.CASCADE)
	service     = models.ForeignKey(Service, on_delete=models.CASCADE)
	
	def __str__(self):
		try:
			return self.function.desc
		except:
			return str(self.id)
	
class Collab(models.Model):
	class Meta:
		db_table='TAB_COLLABS'
		verbose_name = 'Collaborator'
		verbose_name_plural= 'Collaborators'
		admin_site_details 	= {'index':2, 'parent':'Service'}
		
	class Contract(models.TextChoices):
		UNDEFINED   = 'nan', trad('Indéfini')
		CDI         = 'cdi', trad('Contrat à durée indéterminée')
		CDD         = 'cdd', trad('Contrat à durée déterminée')
		APPRENTI    = 'app', trad('Apprentissage')
		INTERIM     = 'int', trad('Interim')
		PRESTA      = 'presta', trad('Prestation')
		
	tgm         = models.CharField('Trigramme', max_length=5, unique=True)
	name        = models.CharField('NOM Prénom', max_length=200)
	email       = models.EmailField('Email', max_length=100)
	job         = models.ForeignKey(Job, null=True, on_delete=models.SET_NULL)
	activ       = models.BooleanField('Actif', default=True)
	start_at    = models.DateField('début')
	end_at      = models.DateField('Fin', null=True)
	contract    = models.CharField('Contrat',
		max_length=16, 
		choices = Contract.choices,
		default = Contract.UNDEFINED)
	manager     = models.ForeignKey(to='Collab', null=True, on_delete=models.SET_NULL)
	
	
	def __str__(self):
		return self.name
 
'''-------------------------	Specif		---------------------------'''
class Specif(models.Model):
	class Meta:
		db_table='TAB_SPECIFS'
		verbose_name = 'Specification'
		verbose_name_plural= 'Specifications'
		admin_site_details 	= {'index':1000}
		
	class TypeSpecif(models.TextChoices):
		UNDEFINED   = 'nan', trad('Indéfini')
		POSITION    = 'pos', trad('Position')
		MESURE      = 'mes', trad('Mesure')
		PRESSION    = 'press', trad('Pression')
		FREQUENCE    = 'freq', trad('Fréquence')
		
	class Unit(models.TextChoices):
		NONE   = 'none', trad('Sans')
		MM  = 'mm', trad('millimètres')
		M   = 'm',  trad('mètre')
		BAR = 'bar', trad('bar')
		HZ = 'hz', trad('Hz')
		
	#Cette table liste toute les specifications d'une ligne: dans le cas d'un process Fond, il s'agira du diam
	desi    = models.CharField('désignation', max_length=16, unique=True)
	desc    = models.CharField('description', max_length=200, default='')
	
	typespecif  = models.CharField(
		max_length=16, 
		choices = TypeSpecif.choices,
		default = TypeSpecif.UNDEFINED)
	
	unit    = models.CharField(
		max_length=16, 
		choices = Unit.choices, 
		default = Unit.NONE)

	def __str__(self):
		return self.desi
	
	def __unicode__(self):
		return self.desi

class Specific_Value(models.Model):
	class Meta:
		db_table='TAB_SPECIFIC_VALUES'
		verbose_name_plural= 'Specific Values'
		constraints = [
			models.UniqueConstraint(fields=['specif', 'value'], name = 'unique specific value')
			]
		admin_site_details 	= {'index':1, 'parent':'Specif'}

	specif  = models.ForeignKey(Specif, on_delete = models.CASCADE)
	value   = models.FloatField(default=0.0)

	def __str__(self):
		return self.specif.desi

'''-------------------------	Process		---------------------------''' 
class Process(models.Model):
	class Meta:
		db_table='TAB_PROCESS'
		verbose_name = "Procédé"
		verbose_name_plural = "Process"
		admin_site_details 	= {'index':1, 'parent':'ProdLine'}
	
	desi    = models.CharField('désignation', max_length=16, unique=True)
	desc    = models.CharField('description', max_length=200, default='')
	group_des = models.CharField('désignation group', max_length=16, null =True)
	
	def __str__(self):
		return self.desi

'''-------------------------	ProdLine		---------------------------'''
class ProdLine(models.Model):
	class Meta:
		db_table='TAB_PRODLINES'
		verbose_name = "Ligne de production"
		verbose_name_plural = "Production Lines"
		admin_site_details 	= {'index':3}
		
	class Statut(models.IntegerChoices):
		RUNNING = 2 , trad('En fonctionnement')
		PRODUCING = 3 , trad('En Production')
		CLOSED  = 0 , trad('Fermée')
		MAINTENANCE = 20 , trad('En maintenance')
		STOPPED = 1 , trad('Arrêtée')
		WAITING = 10 , trad('En attente')
		
	desi    = models.CharField(max_length=16, unique=True)
	desc    = models.CharField(max_length=200, default='')
	wshop   = models.ForeignKey(WShop, null=True, on_delete = models.SET_NULL)
	specifs = models.ManyToManyField(Specific_Value, through='ProdLine_Specific_Value')
	process   = models.ForeignKey(Process, null=True, on_delete = models.SET_NULL)
	statut = models.IntegerField(
		choices = Statut.choices,
		default = Statut.MAINTENANCE)
	cur_speed = models.IntegerField(default=0)
	
	def __str__(self):
		return self.desi
		
class ProdlineStatus_Change(models.Model):
	class Meta:
		db_table='TAB_PRODLINESTATUS_CHANGES'
	
	prodline = models.ForeignKey(ProdLine, on_delete = models.CASCADE)
	previous_status = models.CharField(
		max_length=16, 
		choices = ProdLine.Statut.choices,
		default = ProdLine.Statut.STOPPED)
	new_status = models.CharField(
		max_length=16, 
		choices = ProdLine.Statut.choices,
		default = ProdLine.Statut.RUNNING)
	recorded_at = models.DateTimeField(verbose_name ='enregistrement')
		 
class ProdLine_Specific_Value(models.Model):
	class Meta:
		db_table='TAB_PRODLINE_SPECIFIC_VALUES'
	specifvalue  = models.ForeignKey(Specific_Value, on_delete=models.CASCADE)
	prodline = models.ForeignKey(ProdLine, on_delete=models.CASCADE)

'''-------------------------	Equipment		---------------------------'''
class Equipment_Role(models.Model):
	class Meta:
		db_table='TAB_EQUIPMENT_ROLES'
		verbose_name = 'Role équipement'
		verbose_name_plural = 'Equipment Categories'
		admin_site_details 	= {'index':1, 'parent':'Equipment'}
	
	group   = models.CharField(max_length=32) 
	detail  = models.CharField(max_length=32)    
	desc    = models.CharField(max_length=200, unique=True)  
	
	'''
	img_extention= models.CharField(max_length=12, default='.jpeg')
	'''
	def __str__(self):
		return self.group
		
class Equipment(models.Model):
	class Meta:
		db_table='TAB_EQUIPMENTS'
		verbose_name = "Equipement"
		verbose_name_plural = "Equipments"
		admin_site_details 	= {'index':4}
	
	class Condition(models.TextChoices):
		UNDEFINED = 'Undefined', trad('Undefined')
		FF = 'Fully Functional', trad('Fully Functional')
		FO = 'Full Overhaul', trad('Full Overhaul')
		AN = 'As New', trad('As New')
		MR = 'Minor Repair', trad('Minor Repair')
		SO = 'Scrap/Spares Only', trad('Scrap/Spares Only')
	class Status(models.TextChoices):
		UNDEFINED = 'Undefined', trad('Undefined')
		S  = 'Surplus', trad('Surplus')
		A  = 'Standalone', trad('Standalone')
		O  = 'Operational', trad('Operational')
	class EquiType(models.TextChoices):
		UNDEFINED   = 'Undefined', trad('Undefined')
		LINE        = '1', trad('Ligne de production')
		QUALITY     = '4', trad('Qualité')
	
	model       = models.CharField(max_length=200, null = True)
	manufact    = models.CharField(max_length=200, null = True)
	detail      = models.CharField(max_length=2000, null = True)
	condition   = models.CharField(max_length=32, choices = Condition.choices, default = Condition.UNDEFINED) 
	status      = models.CharField(max_length=32, choices = Status.choices, default = Status.UNDEFINED)
	equitype    = models.CharField(max_length=32, choices = EquiType.choices, default = EquiType.UNDEFINED)
	process     = models.ForeignKey(Process, null = True, on_delete = models.SET_NULL)
	role        = models.ForeignKey(Equipment_Role, null = True, on_delete = models.SET_NULL)
	prodline    = models.ForeignKey(ProdLine, null = True, on_delete = models.SET_NULL)
	wshop       = models.ForeignKey(WShop, null = True, on_delete = models.SET_NULL)
	#desi        = models.CharField(max_length=200)
	owner       = models.ForeignKey(Service, null=True, on_delete = models.SET_NULL)
	running     = models.BooleanField(default=True)
	installed_at= models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		try:
			return "{} - {} - {}".format(self.prodline.desi, self.role.group, self.id)
		except:
			return "equipment {}".format(self.id)
		
