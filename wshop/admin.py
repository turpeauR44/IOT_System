from django.contrib import admin
from wshop.models import *
import system.models as System
from system.admin import SystemModelAdmin, SystemTabularInline

@admin.register(WShop)
class WShopAdmin(SystemModelAdmin):
	class ProdLineInline(SystemTabularInline):
		verbose_name = "Ligne de production"
		verbose_name_plural = "Lignes de production"
		model = ProdLine
		show_change_link = True
		fieldsets = [
			(None,{'fields':['desi', 'desc']})
			]
		readonly_fields=['desi', 'desc']
		extra = 0
	list_display = ('desc', 'desi')
	inlines = [ProdLineInline,]

'''-------------------------	Collab		---------------------------'''
@admin.register(Service)
class ServiceAdmin(SystemModelAdmin):
	class JobInline(SystemTabularInline):
		model = Job
		show_change_link = True
		fields=('function',)
		extra = 0
	list_display = ('desc', 'desi')
	inlines = [JobInline,]
@admin.register(Function)
class FunctionAdmin(SystemModelAdmin):
	class JobInline(SystemTabularInline):
		model = Job
		show_change_link = True
		fields=('service',
		)
		readonly_fields=['service',]
		extra = 0
	list_display = ('desc', 'desi')
	inlines = [JobInline,]
@admin.register(Job)	
class JobAdmin(SystemModelAdmin):
	class CollabInline(SystemTabularInline):
		model = Collab
		show_change_link = True
		#fields=('tgm',)
		#readonly_fields=['name', 'job']
		extra = 0
	list_display = ('function', 'service')
	inlines = [CollabInline,]
@admin.register(Collab)	
class CollabAdmin(SystemModelAdmin):
	pass
'''-------------------------	Specif		---------------------------'''

'''-------------------------	Process		---------------------------''' 

'''-------------------------	ProdLine		---------------------------'''
@admin.register(ProdLine)
class ProdLineAdmin(SystemModelAdmin):
	class EquipmentInline(SystemTabularInline):
		verbose_name = "Equipment"
		verbose_name_plural = "Equipments"
		model = Equipment
		show_change_link = True
		fields=('id', 'role', 'model', 'detail')
		readonly_fields=['id', 'role', 'model', 'detail']
		extra = 0
	inlines = [EquipmentInline,]
	list_display = ('desi', 'desc')
	
'''-------------------------	Equipment		---------------------------'''
@admin.register(Equipment)
class EquipmentAdmin(SystemModelAdmin):
	class SystemIOInline(SystemTabularInline):
		verbose_name = "IO"
		verbose_name_plural = "IOS"
		model = System.IO
		show_change_link = True
		fields=('controller', 'put', 'type')
		readonly_fields=['controller', 'put', 'type']
		extra = 0
	#list_filter = (('wshop', admin.RelatedOnlyFieldListFilter),)
	inlines = [SystemIOInline,]

