from inoutput.models.import *
from IOT.log import write as log_write, return_Debug
from system.management.functions.utils import date_now

class Processus():
	def __init__(self,obj):
		self.debug 			= return_Debug()
		self.equipment 		= obj.guest
		self.controllers 	= [controller(obj) for obj in Controller.objects.using('system').filter(guest=obj.guest)]
	
	def Loop(self):
		for controller in self.controllers:
			controller.Loop()

class controller():
	def __init__(self,obj):
		self.obj 		= obj		
		self.debug 		= return_Debug()
		self.dig_inputs = self.exist_io('in', 'digital') 
		self.ana_inputs = self.exist_io('in', 'analog')
		self.logtypes	= Log_Type.get_logtypes_dict()
		self.logs		= self.log_TypePut_dict()
		
		if self.debug: log_write("configuration : {}".format(self.get_config(type='digital', put='in')))
		
		self.controller_com()
		
		if self.debug: log_write("configuration controller : {}".format(controller_write_read(self,0)))
	
	def Loop(self):
		if self.dig_inputs : feedback1 = controller_write_read(self,1)
		if self.ana_inputs : feedback2 = controller_write_read(self,2)
		controller_write(self,0)
		if self.dig_inputs : self.record(feedback1, io_type='digital', io_put='in')
		if self.ana_inputs : self.record(feedback2, io_type='analog', io_put='in')
		
	def exist_io(self,Type,Put):
		return (len(IO.objects.using('system').filter(controller=self.obj, put=Put, type=Type))>0) 
	
	def log_TypePut_dict(self):
		#L'idée est de prélister les logs concernés par le controller
		Dict={}
		for TypePut in self.logtypes.keys():
			Dict[TypePut]={}
			for logtype in self.logtypes[TypePut]:
				TypeSubtype = "{}{}".format(logtype.type, logtype.subtype)
				Dict[TypePut][TypeSubtype] = Log.objects.using('system').filter(log_type= logtype, io__controller=self.obj).order_by('io__pin')
		return Dict
	
	def controller_com(self):
		self.com = serial.Serial(self.obj.serial, self.obj.baud)
		time.sleep(2)
		
	def controller_write(self,code):
		self.com.write(str(code).encode())
		
	def controller_write_read(mycontroller,code):
		self.com.write(str(code).encode())
		time.sleep(0.1)
		return controller_read(self)

	def controller_read(self):
		return '{}'.format(self.com.readline()).replace("b'","").replace("\\r\\n'","")
	
	def get_config(self, type, put):
		inputs = IO.objects.using('system').filter(controller=self.obj, type=type, put=put)
		
		in_config = '0/{}/{}'.format(	self.obj.period,
										(';').join([myinput.pin for myinput in inputs]))
		if type=='digital':
			in_config +='/{}/{}/0'.format(	(';').join([str(Digital_IO.objects.using('system').get(io=myinput).initial) for myinput in inputs]),
											self.transcript_book(type, put))
		return in_config
	
	def transcript_book(self, io_type, io_put):
		cnt_log_type=0
		txt = ""
		
		TypePut = "{}{}".format(io_type,io_put)
		for logtype in self.logtypes[TypePut]:
			Logs = Log.objects.using('system').filter(log_type = logtype, io__controller=self.obj)
			if cnt_log_type>0: txt += '#'
			cnt_log_type += 1
			cnt_io = 0
			for log in Logs:
				if cnt_io>0: txt += ';'
				cnt_io +=1
				txt += log.io.pin
		return txt
	
	def record(self, feedback, io_type, io_put):
		
		data 		= feedback.split('/')
		count 		= data[1]
		time_lapsed = data[2]
		book_logs 	= data[3].split('#')
		if self.debug: print(book_logs)
		
		try:
			last_book = Book.objects.filter(controller=self.obj, io_type=io_type, io_put=io_put).latest('id')
		except:
			last_book = False
		
		book = Book.objects.create(controller=self.obj, timestamp=date_now, duration=time_lapsed, io_type=io_type, io_put=io_put)
		
		
		TypePut = "{}{}".format(io_type,io_put)
		for logtype, book_log in zip(self.logtypes[TypePut], book_logs):
			TypeSubtype = "{}{}".format(logtype.type, logtype.subtype)
			for log, data in zip(self.logs[TypePut][TypeSubtype], book_log.split(';')):
				log_book_create = False
				value=-1
				values=[]
				if log.log_type.subtype=="Value":
					if data!='': value = int(data)
				else:
					data = transformed_data(data)
					if log.log_type.subtype=="Range" and len(data)==3:
						value = data[1]
						values= [data[0], data[2]]
					elif log.log_type.subtype=="Full"and len(data)>1:
						value = get_average(data)
						values= data
				if value >= 0:
					if last_book:
						try:
							last_log_books = Log_Books.objects.get(last_book=last_book.id, log_value__log=log)
							last_value = last_log_books.log_value.value
							if abs((last_value-value)/(last_value+1))<0.005:
								last_log_books.last_book=book.id
								last_log_books.save()
							else:
								log_book_create = True
						except:
							log_book_create = True
					else:
						log_book_create = True
					if log_book_create:
						log_value = Log_Value.objects.get_or_create(log=log, value=value)
						last_log_books = Log_Books.objects.create(first_book=book.id,last_book=book.id, log_value=log_value[0])
					
					for value in values:
						Value.objects.create(value=value, log_books=last_log_books)

