#!/usr/bin/python3
import sys


tab 			=lambda nb, txt: "".join([ "\t" for i in range(nb-(len(txt))//8)])
def txt_Dict(key, value):
	if key[0] != "_": sys.stdout.write("\t" + bcolors.BOLD + key + " : " + tab(3,key + " : ") + bcolors.NEUTRAL + str(value) + "\n")
def txt_title(txt):
	sys.stdout.write(bcolors.TAB_HEADER + txt + bcolors.ENDC+ "\n")
def txt_subtitle1(txt):
	sys.stdout.write("   " + bcolors.TAB_HEADER1 + txt + bcolors.ENDC+ "\n")				
def txt_subtitle2(txt):
	sys.stdout.write("\t" + bcolors.TAB_HEADER2 + txt + bcolors.ENDC+ "\n")				
def txt_subtitle3(txt):
	sys.stdout.write("\t    " + bcolors.TAB_HEADER3 + txt + bcolors.ENDC+ "\n")								
def txt_Step(txt, step):
	sys.stdout.write(bcolors.HEADER + "Step:{} \t\t".format(step)+ bcolors.WHITE + bcolors.BOLD + txt + bcolors.ENDC + "\n")
def txt_StepFailed(step):
	sys.stdout.write(bcolors.FAIL + "STOP: Configuration failed at Step: " + bcolors.NEUTRAL + str(step) + "\n")	
def txt_Proceed(txt):
	sys.stdout.write(bcolors.UNDERLINE + "  Proceed:\t"+ bcolors.ENDC + txt + "\t...")		
def txt_Todo():
	sys.stdout.write(bcolors.TODO + "To develop\n" + bcolors.NEUTRAL)
def txt_OK():
	sys.stdout.write(bcolors.OKGREEN + "OK\n" + bcolors.NEUTRAL)
def txt_NOK(txt=""):
	sys.stdout.write(bcolors.FAIL + "NOK "+ txt+ "\n" + bcolors.NEUTRAL)			
def txt_Request(txt):
	sys.stdout.write(bcolors.QUESTION + "Request : " + bcolors.NEUTRAL + txt + "\t")	
def txt_Present(txt):
	sys.stdout.write("\n" + bcolors.BOLD + txt + bcolors.NEUTRAL + "\n")	
def txt_Warning(txt):
	sys.stdout.write(bcolors.BOLD + bcolors.WARNING + "WARNING : " + bcolors.NEUTRAL+ bcolors.WARNING + txt + bcolors.NEUTRAL + "\n")

def Confirm(txt):
	input_OK = False
	txt_Request(txt + " [y/n] ? : ")
	while not input_OK:
		inp = input()
		if inp == "y": 
			return True
		if inp == "n": 
			return False
		else : 
			txt_Request("you have to choose [y/n] : ")			

def Select(select_List, txt):
	select_ok = False
	cnt = 0
	for item in select_List:
		sys.stdout.write("\t" + bcolors.BOLD + str(cnt) + "\t<--------\t" + bcolors.NEUTRAL + item + "\n")
		cnt+=1
	while not select_ok:
		txt_Request("Select {} between 0 and {}, \"e\" to exit ".format(txt, len(select_List)-1))
		inp = input()
		try : inp=int(inp)
		except: pass
		if inp in range(len(select_List)):
			return inp
		if inp == "e":
			return "exit"


class bcolors:
	HEADER = '\033[1m\033[95m'
	OKBLUE = '\033[94m'
	OKCYAN = '\033[96m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'
	NEUTRAL = '\033[m'
	QUESTION = TODO = '\033[33m'
	TAB_HEADER='\033[94m'
	TAB_HEADER1='\033[96m'
	TAB_HEADER2='\033[1m\033[97m'
	TAB_HEADER3='\033[1m'
	WHITE='\033[97m'
	
	noir='\033[30m'
	rougefonce='\033[31m'
	stop=rougefonce
	rose='\033[91m'
	vertfonce='\033[32m'
	processing=vertfonce
	vertclair='\033[92m'
	orange='\033[33m'
	jaune='\033[93m'
	step=jaune
	bleufonce='\033[34m'
	bleuclair='\033[94m'
	violetfonce='\033[35m'
	violetclair='\033[95m'
	value=violetclair
	cyanfonce='\033[36m'
	cyanclair='\033[96m'
	grisclair='\033[37m'
	result=WHITE
