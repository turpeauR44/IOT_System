from wshop.models import *
from django.contrib.auth.models import User
from datetime import datetime

def get_Extractions(model):
	Dict = {'wshop':[		{'fct':WShop_extract            , 'class': WShop            , 'File': 'WShops.csv'},],
			'collab':[		{'fct':Function_extract         , 'class': Function         , 'File': 'Functions.csv'},
							{'fct':Service_extract          , 'class': Service          , 'File': 'Services.csv'},
							{'fct':Collab_extract           , 'class': Collab           , 'File': 'Collabs.csv'},],
			'specif':[		{'fct':Specif_extract           , 'class': Specif           , 'File': 'Specifs.csv'},
							{'fct':Specific_Value_extract   , 'class': Specific_Value   , 'File': 'Specific_values.csv'},],
			'process':[		{'fct':Process_extract          , 'class': Process          , 'File': 'Process.csv'},],
			'prodline':[	{'fct':ProdLine_extract         , 'class': ProdLine         , 'File': 'Prodlines.csv'},
							{'fct':ProdLine_Specific_Value_extract, 'class': ProdLine_Specific_Value  	, 'File': 'ProdLine_Specific_Values.csv'},],
			'equipment':[	{'fct':Equipment_Role_extract   , 'class': Equipment_Role   , 'File': 'Equipment_roles.csv'},
							{'fct':Equipment_extract        , 'class': Equipment        , 'File': 'Equipments.csv'},],
						#{'fct':Project_extract          , 'class': Project           , 'File': 'Projects.csv'},
						#{'fct':EventType_extract        , 'class': EventType         , 'File': 'Eventtypes.csv'},
						#{'fct':ProjectLabel_extract     , 'class': ProjectLabel      , 'File': 'Projectlabels.csv'},
						#{'fct':Event_extract            , 'class': Event             , 'File': 'Events2.csv'          , 'file_type': 'extract_access' , 'refresh': False},
						}
	return Dict[model]
def get_Exports(model):
	Dict = {'wshop':[		{'fct':WShop_export            , 'class': WShop             , 'File': 'WShops.csv'},],
			'collab':[		{'fct':Function_export         , 'class': Function          , 'File': 'Functions.csv'},
							{'fct':Service_export          , 'class': Service           , 'File': 'Services.csv'},
							{'fct':Collab_export           , 'class': Collab            , 'File': 'Collabs.csv'},],
			'specif':[		{'fct':Specif_export           , 'class': Specif            , 'File': 'Specifs.csv'},
							{'fct':Specific_Value_export   , 'class': Specific_Value    , 'File': 'Specific_values.csv'},],
			'process':[		{'fct':Process_export          , 'class': Process           , 'File': 'Process.csv'},],
			'prodline':[	{'fct':ProdLine_export         , 'class': ProdLine          , 'File': 'Prodlines.csv'},
							{'fct':ProdLine_Specific_Value_export, 'class': ProdLine_Specific_Value   	, 'File': 'ProdLine_Specific_Values.csv'},],
			'equipment':[	{'fct':Equipment_Role_export   , 'class': Equipment_Role    , 'File': 'Equipment_roles.csv'},
							{'fct':Equipment_export        , 'class': Equipment         , 'File': 'Equipments.csv'},],
						#{'fct':Project_export          , 'class': Project           , 'File': 'Projects.csv'},
						#{'fct':EventType_export        , 'class': EventType         , 'File': 'Eventtypes.csv'},
						#{'fct':ProjectLabel_export     , 'class': ProjectLabel      , 'File': 'Projectlabels.csv'},
						#{'fct':Event_export            , 'class': Event             , 'File': 'Events2.csv'          , 'file_type': 'export_access' , 'refresh': False},
						}
	return Dict[model]

None_feed_id		=lambda x: "" if not x else x.id
None_feed_desi		=lambda x: "" if not x else x.desi
None_feed_tgm		=lambda x: "" if not x else x.tgm
None_feed_group_des	=lambda x: "" if not x else x.group_des

'''-------------------------	WShop		---------------------------'''
#	WShop
def WShop_extract(file_extract, Debug=False, **kwargs):
	for wshop in file_extract['rows']:
		ws = WShop.objects.using('system').create(desi = wshop['desi'], desc = wshop.get('desc',""))
		if Debug : print('l\'atelier {} a été créé'.format(ws.desi))
def WShop_export(file_export, Debug=False, **kwargs):
	with open(file_export, 'w') as exported_file:
		exported_file.write('desi;desc\n')
		for ws in WShop.objects.using('system').all():
			exported_file.write('{};{}\n'.format(ws.desi, ws.desc))
			if Debug : print('l\'atelier {} a été exporté'.format(ws.desi))

'''-------------------------	Collab		---------------------------'''
#	Function   
def Function_extract(file_extract, Debug=False, **kwargs):
	for function in file_extract['rows']:
		fct = Function.objects.using('system').create(desi = function['desi'], desc = function.get('desc',""))
		if Debug : print('la fonction {} a été créée'.format(fct.desi))
def Function_export(file_export, Debug=False, **kwargs):
	with open(file_export, 'w') as exported_file:
		exported_file.write('desi;desc\n')
		for fct in Function.objects.using('system').all():
			exported_file.write('{};{};\n'.format(fct.desi, fct.desc))
			if Debug : print('la fonction {} a été exportée'.format(fct.desi))
#	Service 
def Service_extract(file_extract, Debug=False, **kwargs):
	for service in file_extract['rows']:
		svc = Service.objects.using('system').create(desi = service['desi'], desc = service.get('desc',""))
		if service.get('relates_to',None)!=None and service['relates_to']!="":
			svc.relates_to=Service.objects.using('system').get(desi=service['relates_to'])
			svc.save()
		if Debug : print('le service {} a été créé'.format(svc.desi))
def Service_export(file_export, Debug=False, **kwargs):
	with open(file_export, 'w') as exported_file:
		exported_file.write('desi;desc;relates_to\n')
		for svc in Service.objects.using('system').all():
			exported_file.write('{};{};{}\n'.format(svc.desi, svc.desc, None_feed_desi(svc.relates_to)))
			if Debug : print('le service {} a été exporté'.format(svc.desi))
#	Collab
def Collab_extract(file_extract, Debug=False, **kwargs):
	for collab in file_extract['rows']:
		
		for contrat in Collab.Contract:
			if contrat == collab['contract']:
				break
		
		if collab.get('manager',"")!="":
			manag = Collab.objects.using('system').get(tgm=collab['manager'])
		else:
			manag = None
		
		if collab['activ']==0:
			end_at = datetime(2019,12,31)
		
		collab = Collab.objects.using('system').create(
			tgm = collab['tgm'], 
			name = collab['name'],
			email= collab['email'],
			start_at = datetime(2018,12,31),
			contract = contrat,
			job=Job.objects.using('system').get_or_create(
				function    = Function.objects.using('system').get(desi=collab['function']),
				service     = Service.objects.using('system').get(desi=collab['service']))[0])
				
		if manag != None: collab.manager = manag
		collab.save()
				
		if Debug : print('le collab {} a été créé'.format(collab.tgm))
def Collab_export(file_export, Debug=False, **kwargs):
	with open(file_export, 'w') as exported_file:
		exported_file.write('tgm;name;email;contract;function;service;manager;activ\n')
		for collab in Collab.objects.using('system').all():
			exported_file.write('{};{};{};{};{};{};{};{}\n'.format(collab.tgm, collab.name, collab.email, collab.contract, collab.job.function.desi, collab.job.service.desi, None_feed_tgm(collab.manager), int(collab.activ)))
			if Debug : print('le collab {} a été exporté'.format(collab.tgm))

'''-------------------------	Specif		---------------------------'''
# Specif
def Specif_extract(file_extract, Debug=False, **kwargs):
	for specif in file_extract['rows']:
		sp = Specif.objects.using('system').create(desi = specif['desi'], desc = specif.get('desc',""))
		for unit in sp.Unit:
			if unit == specif['unit']:
				sp.unit = unit
				break
		for typespecif in sp.TypeSpecif:
			if typespecif == specif['typespecif']: 
				sp.typespecif = typespecif
				break
		sp.save()
		if Debug : print('la specification {} a été créée'.format(sp.desi))
def Specif_export(file_export, Debug=False, **kwargs):
	with open(file_export, 'w') as exported_file:
		exported_file.write('desi;desc;unit;typespecif\n')
		for sp in Specif.objects.using('system').all():
			exported_file.write('{};{};{};{}\n'.format(sp.desi, sp.desc, sp.unit, sp.typespecif))
			if Debug : print('la specification {} a été exportée'.format(sp.desi))
# Specif_Value
def Specific_Value_extract(file_extract, Debug=False, **kwargs):
	for specific_value in file_extract['rows']:
		sv= Specific_Value.objects.using('system').create(
				specif = Specif.objects.using('system').get(desi=specific_value['specif']),
				value  = specific_value['value'])
def Specific_Value_export(file_export, Debug=False, **kwargs):
	with open(file_export, 'w') as exported_file:
		exported_file.write('specif;value\n')
		for sv in Specific_Value.objects.using('system').all():
			exported_file.write('{};{}\n'.format(sv.specif.desi, sv.value))

'''-------------------------	Process		---------------------------''' 
# Process 
def Process_extract(file_extract, Debug=False, **kwargs):
	for process in file_extract['rows']:
		proc = Process.objects.using('system').create(desi = process['desi'], desc = process.get('desc',""), group_des = process['group_des'])
		if Debug : print('le process {} a été créé'.format(proc.desi))
def Process_export(file_export, Debug=False, **kwargs):
	with open(file_export, 'w') as exported_file:
		exported_file.write('desi;desc;group_des\n')
		for proc in Process.objects.using('system').all():
			exported_file.write('{};{};{}\n'.format(proc.desi, proc.desc, proc.group_des))
		if Debug : print('le process {} a été exporté'.format(proc.desi))

'''-------------------------	ProdLine		---------------------------'''
# ProdLine  
def ProdLine_extract(file_extract, Debug=False, **kwargs):
	for prodline in file_extract['rows']:
		try: wshop = WShop.objects.using('system').get(desi = prodline['wshop'])
		except: wshop = None
		try: process = Process.objects.using('system').get(desi = prodline['process'])
		except: process = None
		prod = ProdLine.objects.using('system').create(	desi = prodline['desi'], 
														desc = prodline['desc'], 
														wshop = wshop,
														process = process)
		if Debug : print('la ligne de production {} a été créée'.format(prod.desi))		
def ProdLine_export(file_export, Debug=False, **kwargs):
	with open(file_export, 'w') as exported_file:
		exported_file.write('desi;desc;wshop;process\n')
		for prodline in ProdLine.objects.using('system').all():
			exported_file.write('{};{};{};{}\n'.format(prodline.desi, prodline.desc, None_feed_desi(prodline.wshop), None_feed_desi(prodline.process)))
			if Debug : print('la ligne de production {} a été exportée'.format(prodline.desi))
# ProdLine_Specific_Value  
def ProdLine_Specific_Value_extract(file_extract, Debug=False, **kwargs):
	for pv in file_extract['rows']:
		pv = ProdLine_Specific_Value.objects.using('system').create(	prodline = ProdLine.objects.using('system').get(desi=pv['prodline']),
																		specifvalue = Specific_Value.objects.using('system').get_or_create(	specif=Specif.objects.using('system').get(desi=pv['specif']),
																																			value=pv['value'])[0])
		if Debug : print('la specif {} de la ligne de production {} a été créée'.format(pv.specifvalue.specif.desi,pv.prodline.desi ))
def ProdLine_Specific_Value_export(file_export, Debug=False, **kwargs):
	with open(file_export, 'w') as exported_file:
		exported_file.write('specif;value;prodline\n')
		for pv in ProdLine_Specific_Value.objects.using('system').all():
			exported_file.write('{};{};{}\n'.format(pv.specifvalue.specif.desi, pv.specifvalue.value,pv. prodline.desi))
			if Debug : print('la specif {} de la ligne de production {} a été exportée'.format(pv.specifvalue.specif.desi,pv.prodline.desi ))

'''-------------------------	Equipment		---------------------------'''
# Equipment_Role         
def Equipment_Role_extract(file_extract, Debug=False, **kwargs):
	for role in file_extract['rows']:
		rol = Equipment_Role.objects.using('system').create(id = int(role['id']), desc = role.get('desc',""), group = role['group'], detail = role.get('detail',"") )
		if Debug : print('le rôle {} a été crée'.format(rol.id))
def Equipment_Role_export(file_export, Debug=False, **kwargs):
	with open(file_export, 'w') as exported_file:
		exported_file.write('id;desc;group;detail\n')
		for rol in Equipment_Role.objects.using('system').all():
			exported_file.write('{};{};{};{}\n'.format(rol.id, rol.desc, rol.group, rol.detail))
			if Debug : print('le rôle {} a été exporté'.format(rol.id))
# Equipment 
def Equipment_extract(file_extract, Debug=False, **kwargs):
	for equipment in file_extract['rows']:            
		equi = Equipment.objects.using('system').get_or_create(id = equipment['id'])
		
		equi = equi[0]
		equi.model =    equipment['model']
		equi.manufact = equipment['manufact']
		equi.condition = equipment['condition']
		for status in Equipment.Status:
			if status == equipment['status']:
				equi.status = status
				break
		for equitype in Equipment.EquiType:
			if equitype == equipment['equitype']:
				equi.equitype = equitype
				break
		
		try: equi.owner = Service.objects.using('system').get(desi = equipment['owner'])
		except: pass
		try: equi.process = Process.objects.using('system').get(group_des=equipment['process'])
		except: pass
		try: equi.role  = Equipment_Role.objects.using('system').get(id = int(equipment['role']))
		except: pass
		try:
			equi.prodline = ProdLine.objects.using('system').get(desi = equipment['prodline'])
			equi.wshop = equi.prodline.wshop
		except: 
			try:
				equi.wshop = WShop.objects.using('system').get(desi = equipment['wshop'])
			except:
				pass
		if Debug : print('l\'équipement {} a été créé'.format(equi.id)) 
		equi.save()
def Equipment_export(file_export, Debug=False, **kwargs):
	with open(file_export, 'w') as exported_file:
		exported_file.write('id;model;manufact;condition;status;equitype;owner;process;role;prodline;wshop\n')
		for equi in Equipment.objects.using('system').all():
			exported_file.write('{};{};{};{};{};{};{};{};{};{};{}\n'.format(equi.id, 
																			equi.model, equi.manufact, equi.condition, equi.status, equi.equitype, 
																			None_feed_desi(equi.owner), None_feed_group_des(equi.process), None_feed_id(equi.role),
																			None_feed_desi(equi.prodline),None_feed_desi(equi.wshop)))
			if Debug : print('l\'équipement {} a été exporté'.format(equi.id))    
