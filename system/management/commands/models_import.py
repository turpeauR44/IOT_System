#! /usr/bin/python3
#	Import des librairies
	#	Standard
import sys
	
	#	Django
from django.core.management.base import BaseCommand, CommandError
from system.management.functions.extract import csv_extract
	#	Projet

from system.management.functions.extract import get_Extractions as system_Extracts
from network.management.functions.extract import get_Extractions as net_Extracts
from software.management.functions.extract import get_Extractions as soft_Extracts
from hardware.management.functions.extract import get_Extractions as hard_Extracts
from host.management.functions.extract import get_Extractions as host_Extracts
from inoutput.management.functions.extract import get_Extractions as inoutput_Extracts
from wshop.management.functions.extract import get_Extractions as wshop_Extracts

Models_Extractions = [	system_Extracts(),
						wshop_Extracts(),
						soft_Extracts(),
						hard_Extracts(),
						net_Extracts(), 
						host_Extracts(),
						inoutput_Extracts(),]

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
		resp_path=input("path du dossier import_data")
		for model_extractions in Models_Extractions:
			resp=input("Souhaitez-vous importer les données liées au modèle {} [y/n]".format(model_extractions['model']))
			path="{}/import_data/{}/".format(resp_path,model_extractions['model'])
			if path[:12]=="/import_data": path=path[1:]
			if resp=="y":
				for extract in model_extractions['list']:
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


