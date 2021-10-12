#! /usr/bin/python3
#	Import des librairies
	#	Standard
import sys
import subprocess

	#	Django
from django.core.management.base import BaseCommand, CommandError
	#	Projet

from system.management.functions.export import get_Exports as system_Exports
from wshop.management.functions.export 	import get_Exports as wshop_Exports

Models_Exports = {		'system'	:{'func':system_Exports, 	'list': ['system', 'network', 'hardware', 'software', 'host', 'inoutput']},
						'wshop'		:{'func':wshop_Exports, 	'list': ['wshop','collab','specif','process','prodline','equipment']},
						}

class Command(BaseCommand):
	help = 'Commande de lancement de l\'import des data csv pour alimenter les tables software'
	def add_arguments(self, parser):
		parser.add_argument('-d', dest='debug', action='store_true')
	def handle(self, *args, **options):
		global Debug
		# Gestion du mode debug en passant l'argument debug
		Debug = options['debug']
		export_folder='{}/import_data'.format(sys.path[0])
		
		for model_export_list in Models_Exports.keys():
			func_export = Models_Exports[model_export_list]['func']
			grouplist_export = Models_Exports[model_export_list]['list']
			
			resp=input("Souhaitez-vous exporter les données liées au modèle {} [y/n]".format(model_export_list))
			
			if resp=="y":
				for group_export in grouplist_export:
					for export in func_export(group_export):
						export['fct']("{}/{}/{}/{}".format(export_folder, model_export_list, group_export, export['File']), Debug = Debug)
						
