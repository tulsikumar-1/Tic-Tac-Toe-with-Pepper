import sys
import random
import os, qi
import subprocess
import time
import json
import pyttsx


pdir = os.getenv('PEPPER_TOOLS_HOME')
sys.path.append(pdir+ '/cmd_server')
import my_pepper_cmd as pepper_cmd
from my_pepper_cmd import *



def speak(text):
    #engine = pyttsx.init()
    #engine.say(text)
    #engine.runAndWait()
    pass

def detect():
	with open('names.json', 'r') as file:
	     known_names = json.load(file)
		
	subprocess.call(['python3', '/home/kumar/playground/demo/sample/scripts/face_check2.py'])
	with open('face.json', 'r') as file:
	      face = json.load(file)
		   
	while face[0]==0:
		   s=["Please come closer to me ","I cant see you face properly"]
		   pepper_cmd.robot.say(random.choice(s))
		   pepper_cmd.robot.run_behavior('comecloser/behavior_1')
		   #speak(s)
		   time.sleep(5)
		   subprocess.call(['python3', '/home/kumar/playground/demo/sample/scripts/face_check2.py'])
		   with open('face.json', 'r') as file:
		     face = json.load(file)
		 
	with open('name.json', 'r') as file:
		   name1 = json.load(file)
		
	if len(name1)==0:
		  s="Hello, Please tell me your name:"
		  pepper_cmd.robot.say(s)
		  speak(s)
		  name1 = str(raw_input(""))
		  #print(name1)
		  known_names1=known_names
		  known_names1.append(name1)
		  with open('names.json', 'w') as file:
		    json.dump(known_names1, file)

		   
	with open('name.json', 'w') as file:
		   json.dump([], file)
		#print( name[0])
		
		#print('name: ',name)
	s="Hello "+ str(name1)
	pepper_cmd.robot.say(s)
	speak(s)
	time.sleep(1)
	return True




