#! /usr/bin/python3
#	Import des librairies
	#	Standard
import sys
	
	#	Django
from django.core.management.base import BaseCommand, CommandError
from system.management.functions.export import csv_extract
	#	Projet

from system.management.functions.export import get_Extractions as system_Extracts
from wshop.management.functions.export import get_Extractions as wshop_Extracts

Models_Extractions = {	'system'	:{'func':system_Extracts, 	'list': ['system', 'network', 'hardware', 'software', 'host', 'inoutput']},
						'wshop'		:{'func':wshop_Extracts, 	'list': ['wshop','collab','specif','process','prodline','equipment']},}

class Command(BaseCommand):
	help = 'Commande de lancement de l\'import des data csv pour alimenter les tables software'
	def add_arguments(self, parser):
		parser.add_argument('-d', dest='debug', action='store_true')
	def handle(self, *args, **options):
		global Debug
		# Gestion du mode debug en passant l'argument debug
		Debug = options['debug']
		lim = 100000000
		lim_init = 0
		file_type='csv'
		print("Attention cette fonction import a été configurée avec des noms de tables particuliers \n Il s'agit d'une commande wshop/managements \n les données csv y sont aussi enregistrées")
		resp=input("Attention il s'agit d'une fonction d'initialisation si aucune fonction d'export n'a été réalisée car vous perderez toutes vos modifications \n Si vous souhaitez poursuivre tapez y")
		if resp!="y": raise Exception("les données n'ont pas été importées")
		import_path="{}/import_data".format(sys.path[0])
		
		for model_extraction_list in Models_Extractions.keys():
			func_extract = Models_Extractions[model_extraction_list]['func']
			grouplist_extract = Models_Extractions[model_extraction_list]['list']
			
			resp=input("Souhaitez-vous importer les données liées au modèle {} [y/n]".format(model_extraction_list))
			
			if resp=="y":
				for group_extract in grouplist_extract:
					for extract in func_extract(group_extract):
						path="{}/{}/{}/".format(import_path,model_extraction_list,group_extract)
						
						table = extract['class']._meta.db_table
						if extract.get('refresh',True): 
							extract['class'].objects.using('system').all().delete()
							print('PROCEED: Suppression des éléments de la table {} \t .....\t OK'.format(table))
							
						try:
							extract['fct'](csv_extract('{}{}'.format(path,extract['File']), lim = lim, lim_init = lim_init, Debug = Debug), file_type = file_type, Debug = Debug)
							print('SUCCESS: l\'extraction vers la table {} s\'est effectuée sans échec'.format(table))
						except:
							msg = 'ECHEC: l\'extraction vers la table {} a échouée'.format(table)
							if Debug : 
								raise Exception(msg)
							else:    
								print(msg)


