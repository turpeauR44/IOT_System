from wshop.models import *
from django.contrib.auth.models import User
from datetime import datetime

def get_Extractions():
	return {'model': 'wshop', 
			'list':[{'fct':WShop_extract            , 'class': WShop             , 'File': 'WShops.csv'},
					{'fct':Function_extract         , 'class': Function          , 'File': 'Functions.csv'},
					{'fct':Service_extract          , 'class': Service           , 'File': 'Services.csv'},
					{'fct':Collab_extract           , 'class': Collab            , 'File': 'Collabs.csv'},
					{'fct':Specif_extract           , 'class': Specif            , 'File': 'Specifs.csv'},
					{'fct':Specific_Value_extract   , 'class': Specific_Value    , 'File': 'Specific_values.csv'},
					{'fct':Process_extract          , 'class': Process           , 'File': 'Process.csv'},
					{'fct':Equipment_Role_extract   , 'class': Equipment_Role    , 'File': 'Equipment_roles.csv'},
					{'fct':ProdLine_extract         , 'class': ProdLine          , 'File': 'Prodlines.csv'},
					{'fct':Equipment_extract        , 'class': Equipment         , 'File': 'Equipments.csv'},
					#{'fct':Project_extract          , 'class': Project           , 'File': 'Projects.csv'},
					#{'fct':EventType_extract        , 'class': EventType         , 'File': 'Eventtypes.csv'},
					#{'fct':ProjectLabel_extract     , 'class': ProjectLabel      , 'File': 'Projectlabels.csv'},
					#{'fct':Event_extract            , 'class': Event             , 'File': 'Events2.csv'          , 'file_type': 'extract_access' , 'refresh': False},
					]}

def WShop_extract(file_extract, Debug=False, **kwargs):
    for wshop in file_extract['rows']:
        ws = WShop.objects.using('system').create(desi = wshop['desi'], desc = wshop.get('desc',""))
        if Debug : print('l\'atelier {} a été crée'.format(ws.desi))   
def Function_extract(file_extract, Debug=False, **kwargs):
    for function in file_extract['rows']:
        fct = Function.objects.using('system').create(desi = function['desi'], desc = function.get('desc',""))
        if Debug : print('la fonction {} a été créee'.format(fct.desi))  
def Service_extract(file_extract, Debug=False, **kwargs):
    for service in file_extract['rows']:
        svc = Service.objects.using('system').create(desi = service['desi'], desc = service.get('desc',""))
        
        if service.get('relates_to',None)!=None and service['relates_to']!="":
            svc.relates_to=Service.objects.using('system').get(desi=service['relates_to'])
            svc.save()
        if Debug : print('le service {} a été créé'.format(svc.desi))
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
            if Debug : print('la specification {} a été créee'.format(sp.desi))
def Specific_Value_extract(file_extract, Debug=False, **kwargs):
    for specific_value in file_extract['rows']:
        sv= Specific_Value.objects.using('system').create(
                specif = Specif.objects.using('system').get(desi=specific_value['specif']),
                value  = specific_value['value'])  
def Process_extract(file_extract, Debug=False, **kwargs):
    for process in file_extract['rows']:
        proc = Process.objects.using('system').create(desi = process['desi'], desc = process.get('desc',""), group_des = process['group_des'])
        if Debug : print('le process {} a été créé'.format(proc.desi))  
def ProdLine_extract(file_extract, Debug=False, **kwargs):
    for prodline in file_extract['rows']:
        prod = ProdLine.objects.using('system').get_or_create(desi = prodline['desi'])[0]
        if prodline['desc']!="": prod.desc = prodline['desc']
        if prodline['wshop']!="": prod.wshop = WShop.objects.using('system').get(desi = prodline['wshop'])
        
        if prodline['process']!="": prod.process = Process.objects.using('system').get(desi = prodline['process'])
        if prodline['specif']!="":
            s = Specif.objects.using('system').get(desi = prodline['specif'])
            sv = Specific_Value.objects.using('system').get_or_create(specif = s, value = prodline['value'] )
            prod.specifs.add(sv[0]) 
            
        prod.save()
            
        if Debug : print('la ligne de production {} a été modifiée'.format(prod.desi))          
def Equipment_Role_extract(file_extract, Debug=False, **kwargs):
    for role in file_extract['rows']:
        rol = Equipment_Role.objects.using('system').create(id = int(role['val']), desc = role.get('desc',""), group = role['group'], detail = role.get('detail',"") )
        if Debug : print('le rôle {} a été crée'.format(rol.id)) 
def Equipment_extract(file_extract, Debug=False, **kwargs):
    for equipment in file_extract['rows']:            
        equi = Equipment.objects.using('system').get_or_create(id = equipment['EquipmentID'])
        
        equi = equi[0]
        equi.model =    equipment['Model']
        equi.manufact = equipment['Manufacturer']
        equi.owner = Service.objects.using('system').get(desi = 'PROD')
        for cond in Equipment.Condition:
            if cond == equipment['Condition']:
                equi.condition = cond
                break
        for status in Equipment.Status:
            if status == equipment['OperationalStatus']:
                equi.status = status
                break
        for equitype in Equipment.EquiType:
            if equitype == equipment['EquipmentTypeID']:
                equi.equitype = equitype
                break
        
        if equipment['Process']!='N/A'      : equi.process = Process.objects.using('system').get(group_des=equipment['Process'])
        if equipment['CategoryCode']!='N/A' : equi.role = Equipment_Role.objects.using('system').get(id = int(equipment['CategoryCode']))
        if equipment['ProductionLineID']!='0':
            prodline = ProdLine.objects.using('system').get_or_create(
                #id = equipment['ProductionLineID'], 
                desi = equipment['ProductionLine'].replace('573',''))
            
            if prodline[1] and Debug: 
                print('la ligne de prod {} a été créée'.format(prodline[0].desi))
            equi.prodline = prodline[0]
            equi.wshop = equi.prodline.wshop
        if Debug : print('l\'équipement {} a été créé'.format(equi.id)) 
        equi.save()   
