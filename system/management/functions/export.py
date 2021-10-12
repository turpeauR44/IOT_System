from csv import reader as csv_reader
from django.contrib.auth.models import User
from system.models import *

def get_Extractions(model):
	Dict = {'system':[		{'fct':User_extract            	, 'class': User            		, 'File': 'Users.csv'},],
			'network':[		{'fct':System_extract           , 'class': System            	, 'File': 'Systems.csv'},
							{'fct':Network_extract          , 'class': Network           	, 'File': 'Networks.csv'}],
			'hardware':[	{'fct':CPU_extract            	, 'class': CPU             		, 'File': 'CPUs.csv'},
							{'fct':NetworkCard_extract     	, 'class': NetworkCard       	, 'File': 'NetworkCards.csv'},
							{'fct':Host_Network_extract     , 'class': Host_Network      	, 'File': 'Host_Networks.csv'}],
			'software':[	{'fct':OS_extract            	, 'class': OS            		, 'File': 'OS.csv'},
							{'fct':OS_User_extract     		, 'class': OS_User      		, 'File': 'User_OS.csv'},],
			'host':[		{'fct':Host_extract            	, 'class': Host            		, 'File': 'Hosts.csv'},
							{'fct':Guest_Processus_extract  , 'class': Guest_Processus  	, 'File': 'Guest_Processus.csv'},],
			'inoutput':[	{'fct':Controller_extract     	, 'class': Controller 			, 'File': 'Controllers.csv'},
							{'fct':IO_extract            	, 'class': IO           		, 'File': 'IOs.csv'},
							{'fct':Log_Type_extract         , 'class': Log_Type    			, 'File': 'Log_Types.csv'},
							{'fct':Log_extract         		, 'class': Log    				, 'File': 'Logs.csv'},],
	}		
	return Dict[model]
def get_Exports(model):
	Dict = {'system':[		{'fct':User_export            	, 'class': User            		, 'File': 'Users.csv'},],
			'network':[		{'fct':System_export           	, 'class': System            	, 'File': 'Systems.csv'},
							{'fct':Network_export          	, 'class': Network           	, 'File': 'Networks.csv'}],
			'hardware':[	{'fct':CPU_export            	, 'class': CPU             		, 'File': 'CPUs.csv'},
							{'fct':NetworkCard_export     	, 'class': NetworkCard       	, 'File': 'NetworkCards.csv'},
							{'fct':Host_Network_export     	, 'class': Host_Network      	, 'File': 'Host_Networks.csv'}],
			'software':[	{'fct':OS_export            	, 'class': OS            		, 'File': 'OS.csv'},
							{'fct':OS_User_export     		, 'class': OS_User      		, 'File': 'User_OS.csv'},],
			'host':[		{'fct':Host_export            	, 'class': Host            		, 'File': 'Hosts.csv'},
							{'fct':Guest_Processus_export  	, 'class': Guest_Processus  	, 'File': 'Guest_Processus.csv'},],
			'inoutput':[	{'fct':Log_export         		, 'class': Log    				, 'File': 'Logs.csv'},
							{'fct':Log_Type_export         	, 'class': Log_Type    			, 'File': 'Log_Types.csv'},
							{'fct':IO_export            	, 'class': IO           		, 'File': 'IOs.csv'},
							{'fct':Controller_export     	, 'class': Controller 			, 'File': 'Controllers.csv'},
							],
	}		
	return Dict[model]
def csv_extract(csv_file, lim, lim_init, **kwargs):
	columns = []
	rows = []
	delimiter = kwargs.get('delimiter',';')
	
	with open(csv_file) as csv_file: 
		extract = csv_reader(csv_file, delimiter = delimiter)
		line_count = 0
		#if Debug : print(extract)
		for row in extract:
			#if Debug : print(row)
			if line_count == 0:
				columns = row
				line_count +=1
			else:
				Dict = {}
				if line_count > lim_init and line_count < lim:
					for column, val in zip(columns,row):
						Dict[column]=val
					rows.append(Dict)
				else:
					if  line_count < lim : 
						pass
					else:
						break
				line_count +=1
			
		print('nombre de lignes extraites : {}'.format(len(rows)))
		csv_file.close()
		return {'columns':columns, 'rows': rows, 'len': line_count-1 }

'''-------------------------	Système		---------------------------'''
#	User
def User_extract(file_extract, Debug=False, **kwargs):
	for row in file_extract['rows']:
		
		user = User.objects.using('system').get_or_create(username= row['username'])[0]
		user.set_password(row['password'])
		user.is_staff	= row['is_staff']
		user.is_superuser= row['is_superuser']
		user.is_active	= True
		user.save()
		user = User.objects.get_or_create(username= row['username'])[0]
		user.set_password(row['password'])
		user.is_staff	= row['is_staff']
		user.is_superuser= row['is_superuser']
		user.is_active	= True
		user.save() 
		
		if Debug : print('l\'utilisateur {} a été créé'.format(user.username))
def User_export(file_export, Debug=False, **kwargs):
	with open(file_export, 'w') as exported_file:
		exported_file.write('username;password;is_staff;is_superuser\n')
		for user in User.objects.using('system').all():
			exported_file.write('{};{};{};{}\n'.format(user.username, user.password, int(user.is_staff), int(user.is_superuser)))
			if Debug : print('l\'utilisateur {} a été exporté'.format(user.username))

'''-------------------------	Network		---------------------------'''
#	System
def System_extract(file_extract, Debug=False, **kwargs):
	for row in file_extract['rows']:
		sys = System.objects.using('system').create(desi = row['desi'], environnement = row.get('environnement',""), activ = row.get('activ',""))
		if Debug : print('le système {} a été créé'.format(sys.desi))   
def System_export(file_export, Debug=False, **kwargs):
	with open(file_export, 'w') as exported_file:
		exported_file.write('desi;environnement;activ\n')
		for sys in System.objects.using('system').all():
			exported_file.write('{};{};{}\n'.format(sys.desi, sys.environnement, int(sys.activ)))
			if Debug : print('le système {} a été exporté'.format(sys.desi))   
#	Network   
def Network_extract(file_extract, Debug=False, **kwargs):
	for row in file_extract['rows']:
		system = System.objects.using('system').get(desi = row['system'])
		net = Network.objects.using('system').create(desi = row['desi'], type = row['type'], system = system, network = row['network'], netmask = row['netmask'],broadcast=row['broadcast'])
		if Debug : print('le réseau {} a été créé'.format(net.desi)) 
def Network_export(file_export, Debug=False, **kwargs):
	with open(file_export, 'w') as exported_file:
		exported_file.write('desi;type;system;network;netmask;broadcast\n')
		for net in Network.objects.using('system').all():
			exported_file.write('{};{};{};{};{};{}\n'.format(net.desi, net.type, net.system.desi, net.network, net.netmask, net.broadcast))
			if Debug : print('le réseau {} a été exporté'.format(net.desi))
#	Host_Network 
def Host_Network_extract(file_extract, Debug=False, **kwargs):
	for row in file_extract['rows']:
		routed_by = None
		if row['routed_by']: routed_by = NetworkCard.objects.using('system').get(mac_addr = row['routed_by'])
		host_net = Host_Network.objects.using('system').create(networkcard = NetworkCard.objects.using('system').get(mac_addr = row['mac_addr']), 
												network= Network.objects.using('system').get(system = System.objects.using('system').get(desi=row['system']),desi = row['network']),
												IPv4=row['IPv4'],routed_by = routed_by)
		if Debug : print('la liason carte - réseau {} - {} a été créée'.format(host_net.networkcard.cpu.desi , host_net.network)) 
def Host_Network_export(file_export, Debug=False, **kwargs):
	None_feed_routedby=lambda x: "" if not x else x.mac_addr
	with open(file_export, 'w') as exported_file:
		exported_file.write('mac_addr;system;network;IPv4;routed_by\n')
		for host_net in Host_Network.objects.using('system').all():
			exported_file.write('{};{};{};{};{}\n'.format(host_net.networkcard.mac_addr, host_net.network.system.desi, host_net.network.desi, host_net.IPv4, None_feed_routedby(host_net.routed_by)))
			if Debug : print('la liason carte - réseau {} - {} a été exportée'.format(host_net.networkcard.cpu.desi , host_net.network)) 

'''-------------------------	Hardware	---------------------------'''
#	CPU
def CPU_extract(file_extract, Debug=False, **kwargs):
	for row in file_extract['rows']:
		cpu = CPU.objects.using('system').create(
					desi = row['desi'],
					model = row['model'])
		if Debug : print('la CPU {} a été créée'.format(cpu.desi)) 
def CPU_export(file_export, Debug=False, **kwargs):
	with open(file_export, 'w') as exported_file:
		exported_file.write('desi;model\n')
		for cpu in CPU.objects.using('system').all():
			exported_file.write('{};{}\n'.format(cpu.desi, cpu.model))	
			if Debug : print('la CPU {} a été exportée'.format(cpu.desi))
#	NetworkCard 
def NetworkCard_extract(file_extract, Debug=False, **kwargs):
	for row in file_extract['rows']:
		netcard = NetworkCard.objects.using('system').create(
					cpu = CPU.objects.using('system').get(desi = row['cpu']),
					mac_addr=row['mac_addr'],
					type = row['type'],detail=row['detail'])
		if Debug : print('la carte réseau {} - {} a été créée'.format(netcard.cpu.desi , netcard.mac_addr)) 
def NetworkCard_export(file_export, Debug=False, **kwargs):
	with open(file_export, 'w') as exported_file:
		exported_file.write('cpu;mac_addr;type;detail\n')
		for netcard in NetworkCard.objects.using('system').all():
			exported_file.write('{};{};{};{}\n'.format(netcard.cpu.desi, netcard.mac_addr, netcard.type, netcard.detail))	
			if Debug : print('la carte réseau {} - {} a été exportée'.format(netcard.cpu.desi , netcard.mac_addr)) 

'''-------------------------	Software	---------------------------'''
#	OS
def OS_extract(file_extract, Debug=False, **kwargs):
	for row in file_extract['rows']:
		img = OS.objects.using('system').create(
				id=row['id'], 
				hostname = row['hostname'],
				ssh_pub = row['ssh_pub'],
				type = row['type'])
		if Debug : print('l\'image {} a été créée'.format(img.hostname))  
def OS_export(file_export, Debug=False, **kwargs):
	with open(file_export, 'w') as exported_file:
		exported_file.write('id;hostname;ssh_pub;type\n')
		for img in OS.objects.using('system').all():
			exported_file.write('{};{};{};{}\n'.format(img.id, img.hostname, img.ssh_pub, img.type))
			if Debug : print('l\'image {} a été exportée'.format(img.hostname))
#	OS_User
def OS_User_extract(file_extract, Debug=False, **kwargs):
	for row in file_extract['rows']:
		usr_img = OS_User.objects.using('system').create(
				user = User.objects.using('system').get(username = row['user']),
				os= OS.objects.using('system').get(id = row['os']),
				password=row['password'])
		if Debug : print('la liaison user - OS {} - {} a été créée'.format(usr_img.user.username , usr_img.os.hostname))  
def OS_User_export(file_export, Debug=False, **kwargs):
	with open(file_export, 'w') as exported_file:
		exported_file.write('user;os;password\n')
		for usr_img in OS_User.objects.using('system').all():
			exported_file.write('{};{};{}\n'.format(usr_img.user.username, usr_img.os.id, usr_img.password))
			if Debug : print('la liaison user - OS {} - {} a été exportée'.format(usr_img.user.username , usr_img.os.hostname))
			
'''-------------------------	Hôte		---------------------------'''
#	Host
def Host_extract(file_extract, Debug=False, **kwargs):
	for row in file_extract['rows']:
		host = Host.objects.using('system').create(
				os		= OS.objects.using('system').get(id=row['os']), 
				cpu 	= CPU.objects.using('system').get(desi=row['cpu']),
				activ 	= row['activ'])
		if Debug : print('l\'hote {} - {} a été créé'.format(host.os.hostname, host.cpu.desi))  		
def Host_export(file_export, Debug=False, **kwargs):
	with open(file_export, 'w') as exported_file:
		exported_file.write('os;cpu;activ;hostname\n')
		for host in Host.objects.using('system').all():
			exported_file.write('{};{};{};{}\n'.format(host.os.id, host.cpu.desi, int(host.activ),host.os.hostname))
			if Debug : print('l\'hote {} - {} a été exporté'.format(host.os.hostname, host.cpu.desi))
#	Guest_Processus
def Guest_Processus_extract(file_extract, Debug=False, **kwargs):
	for row in file_extract['rows']:
		guest_proc = Guest_Processus.objects.using('system').create(
				guest=Guest.objects.using('system').get_or_create(
					host=Host.objects.using('system').get(os=OS.objects.using('system').get(id = row['host_os']),cpu= CPU.objects.using('system').get(desi=row['host_cpu'])),
					desi=row['desi'],
					type=row['type'])[0],
				processus	=Processus.objects.using('system').get_or_create(desi=row['processus'])[0],
				activ		=row['activ'],
				period		=row['period'])
		if Debug : print('le processus {} du guest {} de l\'hote {} a été créé'.format(guest_proc.processus, guest_proc.guest.desi, guest_proc.guest.host.os.hostname)) 
def Guest_Processus_export(file_export, Debug=False, **kwargs):
	with open(file_export, 'w') as exported_file:
		exported_file.write('host_os;host_cpu;desi;type;processus;activ;period\n')
		for guest_proc in Guest_Processus.objects.using('system').all():
			exported_file.write('{};{};{};{};{};{};{}\n'.format(guest_proc.guest.host.os.id, guest_proc.guest.host.cpu.desi, guest_proc.guest.desi, guest_proc.guest.type, guest_proc.processus.desi, int(guest_proc.activ), guest_proc.period))
			if Debug : print('le processus {} du guest {} de l\'hote {} a été exporté'.format(guest_proc.processus, guest_proc.guest.desi, guest_proc.guest.host.os.hostname)) 

'''-------------------------	InOutput	---------------------------'''
#	Controller
def Controller_extract(file_extract, Debug=False, **kwargs):
	for row in file_extract['rows']:
		µcont = Controller.objects.using('system').create(
				guest 	= Guest.objects.using('system').get(desi = row['guest']),
				desi  	= row['desi'],
				board  	= row['board'],
				baud  	= row['baud'],
				serial  = row['serial'],
				period  = row['period'],
				transfer_dur	= row['transfer_dur'],
				nb_pulsmax 		= row['nb_pulsmax'])
		if Debug : print('le microcontroller {} - {} a été créé'.format(µcont.desi , µcont.guest.desi))  
def Controller_export(file_export, Debug=False, **kwargs):
	with open(file_export, 'w') as exported_file:
		exported_file.write('guest;desi;board;baud;serial;period;transfer_dur;nb_pulsmax\n')
		for µcont in Controller.objects.using('system').all():
			exported_file.write('{};{};{};{};{};{};{};{}\n'.format(µcont.guest.desi, µcont.desi, µcont.board, µcont.baud, µcont.serial, µcont.period, µcont.transfer_dur, µcont.nb_pulsmax))
			if Debug : print('le microcontroller {} - {} a été exporté'.format(µcont.desi , µcont.guest.desi))  
#	IO
def IO_extract(file_extract, Debug=False, **kwargs):
	for row in file_extract['rows']:
		io = IO.objects.using('system').create(
				controller 	= Controller.objects.using('system').get(desi=row['controller']), 
				equipment 	= Equipment.objects.using('system').get(id=row['equipment']), 
				desi 		= row['desi'] ,
				put 		= row['put'],
				type 		= row['type'],
				code 		= row['code'],
				pin 		= row['pin'],)
		if io.type=='digital':
			if io.put=='in':
				io_dig = Digital_IO.objects.using('system').create(io = io,
						Period_Min 	=	row['Period_Min'] ,
						Pulse_Min 	=	row['Pulse_Min'] ,
						Period_Max 	=	row['Period_Max'] ,
						Pulse_Max 	=	row['Pulse_Max'] )
			
			elif io.put=='out': pass
			
		elif io.type=='analog':
			if io.put=='in':
				io_ana = Analog_IO.objects.using('system').create(io = io,
						min = row['min'] ,
						val_min = row['val_min'] ,
						max = row['max'] ,
						val_max = row['val_max'] ,)
			elif io.put=='out': pass
		if Debug : print('l\'IO {} du controller {} a été créée'.format(io.code, io.controller.desi))
def IO_export(file_export, Debug=False, **kwargs):
	with open(file_export, 'w') as exported_file:
		exported_file.write('controller;equipment;desi;put;type;pin;code;initial;Period_Min;Pulse_Min;Period_Max;Pulse_Max;min;val_min;max;val_max\n')
		for io in IO.objects.using('system').all():
			exported_file.write('{};{};{};{};{};{};{};'.format(io.controller.desi, io.equipment.id,io.desi,io.put,io.type,io.pin,io.code))
			if io.type=='digital':
				if io.put=='in':
					digio = Digital_IO.objects.using('system').get(io=io)
					exported_file.write('{};{};{};{};{};;;;\n'.format(digio.initial, digio.Period_Min, digio.Pulse_Min, digio.Period_Max, digio.Pulse_Max))
				elif io.put=='out': pass
			elif io.type=='analog':
				if io.put=='in':
					anaio = Analog_IO.objects.using('system').get(io=io)
					exported_file.write(';;;;;{};{};{};{}\n'.format(anaio.min, anaio.val_min, anaio.max, anaio.val_max))
				elif io.put=='out': pass
			if Debug : print('l\'IO {} du controller {} a été exportée'.format(io.code, io.controller.desi))			
#	Log_Type
def Log_Type_extract(file_extract, Debug=False, **kwargs):
	for row in file_extract['rows']:
		ltype = Log_Type.objects.using('system').create(
					type = row['type'],
					subtype = row['subtype'],
					io_type = row['io_type'],
					io_put = row['io_put'],)
		if Debug : print('Le log_type {} - {} - {} - {} a été créé'.format(ltype.type,ltype.subtype,ltype.io_type,ltype.io_put ))
def Log_Type_export(file_export, Debug=False, **kwargs):
	with open(file_export, 'w') as exported_file:
		exported_file.write('type;subtype;io_type;io_put\n')
		for ltype in Log_Type.objects.using('system').all():
			exported_file.write('{};{};{};{}\n'.format(ltype.type,ltype.subtype,ltype.io_type,ltype.io_put))
			if Debug : print('Le log_type {} - {} - {} - {} a été exporté'.format(ltype.type,ltype.subtype,ltype.io_type,ltype.io_put))
#	Log
def Log_extract(file_extract, Debug=False, **kwargs):
	for row in file_extract['rows']:
		io = IO.objects.using('system').get(equipment=row['equipment'], code=row['code'])
		log = Log.objects.using('system').create(
					io = io,
					log_type=Log_Type.objects.using('system').get(type = row['type'], subtype = row['subtype'], io_type = io.type, io_put= io.put))
		if Debug : print('Le log {} - {} - {} - {} a été créé'.format(log.log_type.type,log.log_type.subtype,io.code,io.controller.desi))
def Log_export(file_export, Debug=False, **kwargs):
	with open(file_export, 'w') as exported_file:
		exported_file.write('equipment;code;type;subtype\n')
		for log in Log.objects.using('system').all():
			exported_file.write('{};{};{};{}\n'.format(log.io.equipment.id,log.io.code,log.log_type.type,log.log_type.subtype))
			if Debug : print('Le log {} - {} - {} - {} a été exporté'.format(log.log_type.type,log.log_type.subtype,log.io.code,log.io.controller.desi))
