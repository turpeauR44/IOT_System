from django.contrib import admin
from system.models import *

admin.site.site_header = "CROWN Admin"
admin.site.site_title = "CROWN Admin Portal"
admin.site.index_title = "Welcome to CROWN Portal"


# Register your models here.
class SystemModelAdmin(admin.ModelAdmin):
    # A handy constant for the name of the alternate database.
    using = 'system'

    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=self.using)

    def get_queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        return super().get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super().formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super().formfield_for_manytomany(db_field, request, using=self.using, **kwargs)
class SystemTabularInline(admin.TabularInline):
    using = 'system'

    def get_queryset(self, request):
        # Tell Django to look for inline objects on the 'other' database.
        return super().get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super().formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super().formfield_for_manytomany(db_field, request, using=self.using, **kwargs)

'''-------------------------	Système		---------------------------'''

'''-------------------------	Network		---------------------------'''
@admin.register(System)
class SystemAdmin (SystemModelAdmin):
#	class Meta:
		
#		 has_add_permission = False
		
	class NetworkInLine(SystemTabularInline):
		verbose_name = "Carte réseau"
		verbose_name_plural = "Cartes réseau"
		model = Network
		show_change_link = True
		fields=('desi', 'type')
		extra = 0
	list_display = ("desi",'environnement', 'activ')
	inlines = [NetworkInLine, ]
@admin.register(Network)
class NetworkAdmin (SystemModelAdmin):
	class Host_NetworkInLine(SystemTabularInline):
		verbose_name = "addresses réseau"
		verbose_name_plural = "addresses réseau"
		model = Host_Network
		show_change_link = True
		fields=('networkcard', 'IPv4', 'routed_by')	
		extra = 0
	list_display = ("system", "desi","type" )
	inlines = [Host_NetworkInLine, ]	
@admin.register(Host_Network)
class Host_NetworkAdmin (SystemModelAdmin):
	list_display=("network","networkcard")

'''-------------------------	Hardware	---------------------------'''
@admin.register(CPU)
class CPUAdmin (SystemModelAdmin):
	class NetworkCardInLine(SystemTabularInline):
		verbose_name = "Carte réseau"
		verbose_name_plural = "Cartes réseau"
		model = NetworkCard
		show_change_link = True
		fields=('cpu', 'mac_addr', 'type', 'detail')	
		extra = 0
	
	list_display = ("desi", "model" )
	inlines = [NetworkCardInLine, ]	
@admin.register(NetworkCard)
class NetworkCardAdmin (SystemModelAdmin):
	class Host_NetworkInLine(SystemTabularInline):
		verbose_name = "addresses réseau"
		verbose_name_plural = "addresses réseau"
		model = Host_Network
		fk_name = 'networkcard'
		show_change_link = True
		fields=('network','IPv4', 'routed_by')	
		extra = 0
	inlines = [Host_NetworkInLine, ]

'''-------------------------	Software	---------------------------'''
@admin.register(OS)
class ImageAdmin (SystemModelAdmin):
	class SoftwareInLine(SystemTabularInline):
		verbose_name = "Logiciel"
		verbose_name_plural = "Logiciel"
		model = OS_Software
		show_change_link = True
		fields=('software', )
		readonly_fields=['software']
		extra = 0
	list_display = ("hostname", "id","type" )
	inlines = [SoftwareInLine, ]	
@admin.register(Software)
class ImageAdmin (SystemModelAdmin):
	list_display = ("desi", )

'''-------------------------	Hôte		---------------------------'''
@admin.register(Host)
class HostAdmin (SystemModelAdmin):	
	class GuestInLine(SystemTabularInline):
		model = Guest
		show_change_link = True
		fields=('desi', 'type')
		extra = 0	
	list_display = ("os", "cpu", 'activ')
	inlines = [GuestInLine, ]
@admin.register(Guest)
class GuestAdmin (SystemModelAdmin):	
	class ProcessusInLine(SystemTabularInline):
		model = Guest_Processus
		show_change_link = True
		fields=('processus', 'activ')
		extra = 0		
	list_display = ( "desi", 'host','type')
	inlines = [ProcessusInLine, ]
@admin.register(Processus)
class ProcessusAdmin (SystemModelAdmin):
	pass

'''-------------------------	InOutput	---------------------------'''
@admin.register(Controller)
class ControllerAdmin (SystemModelAdmin):
	class IOInLine(SystemTabularInline):
		model = IO
		show_change_link = True
		fields=('desi', 'put', 'type')
		extra = 0	
	inlines = [IOInLine, ]
@admin.register(IO)
class IOAdmin (SystemModelAdmin):
	class LogInLine(SystemTabularInline):
		model = Log
		show_change_link = True
		extra = 0
	inlines = [LogInLine, ]
@admin.register(Log_Type)
class LogTypeAdmin (SystemModelAdmin):
	pass
