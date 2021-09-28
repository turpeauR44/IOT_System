from django.contrib import admin
import wshop.models as WM
from system.admin import SystemModelAdmin, SystemTabularInline

@admin.register(WM.ProdLine)
class ProdLineAdmin(SystemModelAdmin):
	class EquipmentInline(SystemTabularInline):
		verbose_name = "Equipment"
		verbose_name_plural = "Equipments"
		model = WM.Equipment
		show_change_link = True
		fields=('id', 'role', 'model', 'detail', 'equitype')
		readonly_fields=['id', 'role', 'model', 'detail', 'equitype']
		extra = 0
	inlines = [EquipmentInline,]
	list_display = ('desi', 'desc')
	
@admin.register(WM.WShop)
class WShopAdmin(SystemModelAdmin):
	class ProdLineInline(SystemTabularInline):
		verbose_name = "Ligne de production"
		verbose_name_plural = "Lignes de production"
		model = WM.ProdLine
		fieldsets = [
			(None,{'fields':['desi', 'desc']})
			]
		extra = 0
	inlines = [ProdLineInline,]

@admin.register(WM.Equipment)
class EquipmentAdmin(SystemModelAdmin):
	list_filter = (('wshop', admin.RelatedOnlyFieldListFilter),)

