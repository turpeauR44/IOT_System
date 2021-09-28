from csv import reader as csv_reader
from django.contrib.auth.models import User

def get_Extractions(model):
	Dict = {'system'	:[	{'fct':User_extract            	, 'class': User            		, 'File': 'Users.csv'},],
			'network'	:[	{'fct':System_extract           , 'class': System            	, 'File': 'Systems.csv'},
							{'fct':Network_extract          , 'class': Network           	, 'File': 'Networks.csv'},
							{'fct':Host_Network_extract     , 'class': Host_Network      	, 'File': 'Host_Networks.csv'}],
			'hardware'	:[	{'fct':CPU_extract            	, 'class': CPU             		, 'File': 'CPUs.csv'},
							{'fct':NetworkCard_extract     	, 'class': NetworkCard       	, 'File': 'NetworkCards.csv'},],
			'software'	:[	{'fct':OS_extract            	, 'class': OS            		, 'File': 'OS.csv'},
							{'fct':OS_User_extract     		, 'class': OS_User      		, 'File': 'User_OS.csv'},],
			'host'		:[	{'fct':Host_extract            	, 'class': Host            		, 'File': 'Hosts.csv'},
							{'fct':Guest_Processus_extract  , 'class': Guest_Processus  	, 'File': 'Guest_Processus.csv'},],
			'inoutput'	:[	{'fct':Controller_extract     	, 'class': Controller 			, 'File': 'Controllers.csv'},
							{'fct':IO_extract            	, 'class': IO           		, 'File': 'IOs.csv'},
							{'fct':Log_Type_extract         , 'class': Log_Type    			, 'File': 'Log_Types.csv'},
							{'fct':Log_extract         		, 'class': Log    				, 'File': 'Logs.csv'},],
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
		
		if Debug : print('l\'utilisateur {} a été créée'.format(user.username))

'''-------------------------	Network		---------------------------'''
def System_extract(file_extract, Debug=False, **kwargs):
	for row in file_extract['rows']:
		sys = System.objects.using('system').create(desi = row['desi'], environnement = row.get('environnement',""), activ = row.get('activ',""))
		if Debug : print('le système {} a été crée'.format(sys.desi))   
def Network_extract(file_extract, Debug=False, **kwargs):
	for row in file_extract['rows']:
		system = System.objects.using('system').get(desi = row['system'])
		net = Network.objects.using('system').create(desi = row['desi'], type = row['type'], system = system, network = row['network'], netmask = row['netmask'],broadcast=row['broadcast'])
		if Debug : print('le réseau {} a été crée'.format(net.desi)) 
def Host_Network_extract(file_extract, Debug=False, **kwargs):
	for row in file_extract['rows']:
		routed_by = None
		if row['routed_by']: routed_by = NetworkCard.objects.using('system').get(mac_addr = row['routed_by'])
		host_net = Host_Network.objects.using('system').create(networkcard = NetworkCard.objects.using('system').get(mac_addr = row['mac_addr']), 
												network= Network.objects.using('system').get(system = System.objects.using('system').get(desi=row['system']),desi = row['network']),
												IPv4=row['IPv4'],routed_by = routed_by)
		if Debug : print('la liason carte - réseau {} - {} a été créée'.format(host_net.networkcard.cpu.desi , host_net.network)) 

'''-------------------------	Hardware	---------------------------'''
def CPU_extract(file_extract, Debug=False, **kwargs):
	for row in file_extract['rows']:
		cpu = CPU.objects.using('system').create(
					desi = row['desi'],
					model = row['model'])
		if Debug : print('la CPU {} a été créée'.format(cpu.desi)) 
def NetworkCard_extract(file_extract, Debug=False, **kwargs):
	for row in file_extract['rows']:
		netcard = NetworkCard.objects.using('system').create(
					cpu = CPU.objects.using('system').get(desi = row['cpu']),
					mac_addr=row['mac_addr'],
					type = row['type'],detail=row['detail'])
		if Debug : print('la carte réseau {} - {} a été créée'.format(netcard.cpu.desi , netcard.mac_addr)) 

'''-------------------------	Software	---------------------------'''
def OS_extract(file_extract, Debug=False, **kwargs):
	for row in file_extract['rows']:
		img = OS.objects.using('system').create(
				id=row['id'], 
				hostname = row['hostname'],
				ssh_pub = row['ssh_pub'],
				type = row['type'])
		if Debug : print('l\'image {} a été créée'.format(img.hostname))  
def OS_User_extract(file_extract, Debug=False, **kwargs):
	for row in file_extract['rows']:
		usr_img = OS_User.objects.using('system').create(
				user = User.objects.using('system').get(username = row['user']),
				os= OS.objects.using('system').get(hostname= row['os']),
				password=row['password'])
		if Debug : print('la liaison user - OS {} - {} a été créée'.format(usr_img.user.username , usr_img.os.hostname))  

'''-------------------------	Hôte		---------------------------'''
def Host_extract(file_extract, Debug=False, **kwargs):
	for row in file_extract['rows']:
		host = Host.objects.using('system').create(
				os		= OS.objects.using('system').get(id=row['os']), 
				cpu 	= CPU.objects.using('system').get(desi=row['cpu']),
				activ 	= row['activ'])
		if Debug : print('l\'hote {} - {} a été créé'.format(host.os.hostname, host.cpu.desi))  		
def Guest_Processus_extract(file_extract, Debug=False, **kwargs):
	for row in file_extract['rows']:
		guest_proc = Guest_Processus.objects.using('system').create(
				guest=Guest.objects.using('system').get_or_create(
					host=Host.objects.using('system').get(os=OS.objects.using('system').get(id = row['host_os']),cpu= CPU.objects.using('system').get(desi=row['host_cpu'])),
					desi=row['desi'],
					type=row['type'])[0],
				processus	=Processus.objects.using('system').get_or_create(desi=row['processus'])[0],
				activ		=row['activ'],
				period		=row['period'],)
		if Debug : print('le processus {} du guest {} de l\'hote {} a été créé'.format(guest_proc.processus, guest_proc.guest.desi, guest_proc.guest.host.os.hostname)) 

'''-------------------------	InOutput	---------------------------'''
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
def Log_Type_extract(file_extract, Debug=False, **kwargs):
	for row in file_extract['rows']:
		ltype = Log_Type.objects.using('system').create(
					type = row['type'],
					subtype = row['subtype'],
					io_type = row['io_type'],
					io_put = row['io_put'],)
		if Debug : print('Le log_type {} - {} - {} - {} a été crée'.format(ltype.type,ltype.subtype,ltype.io_type,ltype.io_put ))
def Log_extract(file_extract, Debug=False, **kwargs):
	for row in file_extract['rows']:
		io = IO.objects.using('system').get(equipment=row['equipment'], code=row['code'])
		log = Log.objects.using('system').create(
					io = io,
					log_type=Log_Type.objects.using('system').get(type = row['type'], subtype = row['subtype'], io_type = io.type, io_put= io.put))
		if Debug : print('Le log {} - {} - {} - {} a été crée'.format(log.log_type.type,log.log_type.subtype,io.code,io.controller.desi))

'''-------------------------	InOutput	---------------------------'''
