import sys
import random
import os, qi
import subprocess
import time
import json
import pyttsx
import json
pdir = os.getenv('PEPPER_TOOLS_HOME')
sys.path.append(pdir+ '/cmd_server')
import my_pepper_cmd as pepper_cmd
from my_pepper_cmd import *
import face_detect
import tic3
import tic4
from webserver import go
import threading
class UserLeavingException(Exception):
    pass




DEBUG=False

sonar_threshold=2
sensor=[0,0]
yes_no = ["yes", "no","sure","no thanks","yes please"]
timeout = 30 # seconds after function returns
sad=True  # to find out is person is sad 
away_sensor=3 # provide a value for distance when user doesnot repond threshold is 2
play=True # used for debug should be always true for game to be played
play_again=True # ask user for play again
change_level_play_again=False # ask user if want to change level
detect=True # used for debug to skip introduction
 # to be defined later tic3 or tic4 object
raw=False # starting from begining for face detection
winner=None
SIMULATION=True

    #recognize move speech
vocabulary4_player_move = ["A 1", "A 2", "A 3","A 4", "B 1", "B 2", "B 3","B 4", "C 1", "C 2", "C 3"," C 4","D 1", "D 2", "D 3","D 4",
                              "1 A", "2 A", "3 A", "1 B", "2 B", "3 B", "1 C", "2 C", "3 C",]

vocabulary3_player_move = ["A 1", "A 2", "A 3", "B 1", "B 2", "B 3", "C 1", "C 2", "C 3",
                              "1 A", "2 A", "3 A", "1 B", "2 B", "3 B", "1 C", "2 C", "3 C",]





if raw==True:
    process1 = subprocess.Popen('python3 Clear_faces.py', shell=True) # delete previous data
    process1.wait()


behaviors=[ 'happy/behavior_1', '.lastUploadedChoregrapheBehavior/behavior_1', 'excited/behavior_1', 'dance3-02e9e0/behavior_1', 'dance2-ac89d9/behavior_1', 'dance-c45fbf/behavior_1', 'congrats/behavior_1', 'confused-0e1db9/behavior_1', 'comecloser/behavior_1', 'bored-2fd67b/behavior_1', 'chill-a3e3e8/behavior_1', 'think1-f42c9d/behavior_1']


start_behave=['happy/behavior_1','excited/behavior_1' ]
pepper_move_behave=['think1-f42c9d/behavior_1','confuse-9344d4/behavior_1','confused-0e1db9/behavior_1']
human_away_behave=['bored-2fd67b/behavior_1','chill-a3e3e8/behavior_1','confuse-9344d4/behavior_1','confused-0e1db9/behavior_1']
human_win=["congrats/behavior_1"]
pepper_win=['dance-c45fbf/behavior_1','dance2-ac89d9/behavior_1','dance3-02e9e0/behavior_1']
come_close=['comecloser/behavior_1']



#pepper_cmd.robot.run_behavior(random.choice(come_close))

def proximity(value):
    away_threshold=2
    if SIMULATION:
     #send = 'python $PEPPER_TOOLS_HOME/sonar/sonar_sim.py --sensor SonarFront --value '+ str(value) +'--duration 20')
     process1 = subprocess.Popen('python $PEPPER_TOOLS_HOME/sonar/sonar_sim.py --sensor SonarFront --value '+ str(value) +' --duration 20', shell=True) 
     time.sleep(2)
     sensor = pepper_cmd.robot.sensorvalue("sonar")
     print(sensor)
    if sensor[0]<away_threshold:
       away=False
    else:
       away=True
    return away


# classes for the webserver

class Blackboard():
    def __init__(self):
        self.the_handler = None
        self.clicked_move = None
        self.game_type = None
    
    def onclick(self, move):
        if not self.clicked_move:
            valid = game.move(*move)
            if valid:
                self.clicked_move = move
                web_board=game.get_board_for_tablet()
                ws_handler.send(web_board)
                pepper_cmd.robot.asr_cancel()   


class WebServerThread(threading.Thread):
    def __init__(self, bb):
        threading.Thread.__init__(self)
        self.bb = bb

    def run(self):
        go(self.bb)


def parse_move(response):
    player_row=None
    player_col=None
    
    if "A" in response:
        player_row = 0
    if "B" in response:
        player_row = 1
    if "C" in response:
        player_row = 2
    if "D" in response:
        player_row = 3
        
        
    if "1" in response:
        player_col = 0
    if "2" in response:
        player_col = 1
    if "3" in response:
        player_col = 2
    if "4" in response:
        player_col = 3
 
    player_move = (player_row, player_col)
    
    return player_move

def get_pepper_move(board,game_plans):
  state=[]
  #print("board:",board)
  for row in board:
    for cell in row:
         state.append('X' if cell == pepper_player else 'O' if cell == human_player else '.')
  #print("state:",state)
  max_score = 0
  best_move = None
  move_index=None
  for plan in game_plans: #access to all plans 
    for  move in plan:  # find next move based on current state # all possible plans are solved using non deterministic action of human
      score = 0
      if state.count(".")==9 and move.count(".")==8: # first move
         score += 1
      elif move.count(".") < state.count(".") and move.count("O") == state.count("O"): # check only succesive possible states
          for item1, item2 in zip(move, state):
              if (item1 == item2 == "O") or (item1 == item2 == "X")  :
                  score += 1
      if score > max_score:
          max_score = score
          best_move = move
  #print(best_move) 
  for index, (item1, item2) in enumerate(zip(best_move, state)):
    if item1 == "X" and item2 == ".":
      
      #print(index)
      row = (index // 3)
      col = (index % 3)

  return (row,col)   


def pepper_turn():
    think_gestures = (
    )   # to be updated
    
    pepper_cmd.robot.say(random.choice((
        "Thinking ...",
        "Let's see...",
        "What to do...?"
    )))
    pepper_cmd.robot.run_behavior(random.choice(pepper_move_behave))
    player_close=None # to be defined
    if player_close:
        pepper_cmd.robot.normalPosture()    # avoid unintentional head drift


    pepper_did_optimal_move=False
    if game_type=="3x":
       if sad:
          pepper_move = random.choice(vocabulary3_player_move)
          pepper_move=parse_move(pepper_move)
       else:
          pepper_move=get_pepper_move(game.board,game_plans)
          pepper_did_optimal_move=True
    else:
          pepper_move = random.choice(vocabulary4_player_move)
          pepper_move=parse_move(pepper_move)          
    

    valid=game.move(*pepper_move)
    if valid:
    # pepper announces its own move. The type of message is simply dictated on
    # whether it picked the optimal move or it went for a more merciful choice.
	    if pepper_did_optimal_move:
		pepper_cmd.robot.say(random.choice((
		    "Then take this!",
		    "Here's my move!"
		)))
	    else:
		pepper_cmd.robot.say(random.choice((
		    "Um, maybe here?",
		    "I'll try this..."
		)))

### end pepper_turn()





def player_turn( pepper_player, human_player): # pepper player X humanplayer 0
    pepper_cmd.robot.say(random.choice(('Your move :)', 'Your turn', 'Go', "What will you do?")))    
    #human move
    pepper_cmd.robot.normalPosture()
    response = ""  # the default response from pepper_cmd's ASR
    impatience_score = 0
    impatience_responses = [
        "Hey, it's your turn",
        "Please, make a move",
        "Come on",
        "Don't think too hard",
        "Just pick a tile",
        "Entering sleep mode... Just kidding."
    ]
    impatience_gestures =  [   ]  #to be updated
    player_move = None
    game_paused = False
    game_pause_countdown = 0
   
    
    away=False
    move_made=False
    while not move_made:

        
        if away:
            pepper_cmd.robot.run_behavior(random.choice(human_away_behave))
            #time.sleep(10)
            #the user left, after 10 seconds the game is paused
            if not game_paused:
                print "user left"
                ws_handler.send("event pause-game")
                game_paused = True
                game_pause_countdown = 3 #countdown to go back to main screen
            if DEBUG: print "countdown: " + str(game_pause_countdown)
            if game_pause_countdown == 1:
                ws_handler.send("event pause-game-warning")
            if game_pause_countdown == 0:
                #raise UserLeavingException("user_left_timeout")
                break
                
            game_pause_countdown -= 1
            
        elif game_paused:
            if  not away:
                #the user came back, the game is resumed
                print "user came back"
                ws_handler.send("event resume-game")
                pepper_cmd.robot.say("Glad to see you back! It's your turn now.")
                game_paused = False
        else:
            
            response = pepper_cmd.robot.asr(vocabulary4_player_move, timeout=5)
            
            # don't do anything else if the move was done via click
            if the_bb.clicked_move:
                player_move = the_bb.clicked_move
                the_bb.clicked_move = None
                move_made=True
                break

            if response:
                player_move = parse_move(response)
                valid = game.move(*player_move)
                if valid:
                    move_made=True
                    break
                    
                else: # invalid move
                    pepper_cmd.robot.say("You can't play there!")
                    print "invalid move"

            else: # ASR timed out
                pepper_cmd.robot.say(impatience_responses[impatience_score])
                impatience_score += 1

                if impatience_score >= len(impatience_responses):
                   impatience_score=1
                   away = proximity(away_sensor)  # value is provided for simulation to show if user left or on real robot it will check sensors and then decide
                   




    optimal_responses = ["Wow, great move!", "You're so good","Are you sure about that?", "Ah, so that's your move", "Nice move","I see", "Okay"]    
      

    if move_made:
        pepper_cmd.robot.say(random.choice(optimal_responses))
    

    return move_made

### end player_turn()



# In which Pepper plays ONE game
# returns the winner: Tris.X, Tris.O, Tris.DRAW
def play_game(game,pepper_player,human_player,game_type):
    print "********************PLAYING******************************"
    ws_handler.send("event loading-start")
    print "initializing game...."
    time.sleep(2)
    pepper_cmd.robot.say("Please wait while I load the game...")

    if game_type == "3x":
	    ws_handler.send("event loading-complete3")
	    # reset highlighting
	    ws_handler.send("highlight .........")
    else:
    	    ws_handler.send("event loading-complete4")
	    # reset highlighting
	    ws_handler.send("highlight ................")
    
    
    	    
    web_board=game.get_board_for_tablet()
    ws_handler.send(web_board)
    
    
    #START MATCH
    game_over=False
    while not game_over:
        move_made=None
        
        if game.get_current_player() == pepper_player:
            pepper_turn()
        else:
            move_made=player_turn(pepper_player, human_player)
            if not move_made:
               break
               
        
        
            
        # update tablet
        web_board=game.get_board_for_tablet()
        ws_handler.send(web_board)
        game_over=game.get_game_over_and_winner()[0]
        if DEBUG: print game

        #check victory
        if game_over:
            break
    #END MATCH

    
    # highlight the tris (if any) on the tablet
    hl_web_board = game.get_tic_highlights_for_tablet()
    ws_handler.send("highlight " + hl_web_board)
    
    return game.get_game_over_and_winner()

### end play_game()






def introduction (detect):
        print "********************USER APPROACHED******************************"
        global sensor
	while detect==False:
	       # sensor = pepper_cmd.robot.sensorvalue("sonar")
		if sensor[0]>sonar_threshold: #frontsonar
		  print("User in front but far")
		  pepper_cmd.robot.say("Please come closer")
		  pepper_cmd.robot.run_behavior(random.choice(come_close))
		  if SIMULATION:
		  	process1 = subprocess.Popen('python $PEPPER_TOOLS_HOME/sonar/sonar_sim.py --sensor SonarFront --value 1.0 --duration 60', shell=True)
		  
		elif sensor[0]<=sonar_threshold and sensor[0]>0: #frontsonar
		  print("User Approached")
		  ws_handler.send("event user-approached")
		  pepper_cmd.robot.green_eyes()
		  pepper_cmd.robot.asay("Hello, I am Pepper")
		  face=False
		  while(face!=True):
		  	face=face_detect.detect()
		  	if face:
		  	 # print("detected")
		  	 pass
		  detect=True
		  ws_handler.send("event show-image")
		  
		elif sensor[1]>0:#back sonar
		  print("User behind")
		  pepper_cmd.robot.headPose(1.6, -0.2,5)
		  pepper_cmd.robot.say("Who is there? Please come infront of me")
		  pepper_cmd.robot.headPose(0, 1.6,5)
		  pepper_cmd.robot.normalPosture()
		  if SIMULATION:
		  	process1 = subprocess.Popen('python $PEPPER_TOOLS_HOME/sonar/sonar_sim.py --sensor SonarFront --value 3.0 --duration 10', shell=True)
	    
		time.sleep(2)
		sensor = pepper_cmd.robot.sensorvalue("sonar")
		print("Sonar sensors",sensor)
		#process1.wait()
	return detect
		

def conversation(detect):
        print "********************FINDING HUMAN MOOD******************************"
	if detect==True:
	       # print("Inside")
		pepper_cmd.robot.asay("How are you?")
		if SIMULATION:
			if sad:
			  subprocess.Popen('python $PEPPER_TOOLS_HOME/asr/human_say.py --sentence "sad"', shell=True)
			else:
			  subprocess.Popen('python $PEPPER_TOOLS_HOME/asr/human_say.py --sentence "good"', shell=True)
		answer = pepper_cmd.robot.asr(["good","sad","not good"],timeout)
		if answer=="sad" or answer=="not good" : # valid answer
		   pepper_cmd.robot.asay("Oh...")
		   pepper_cmd.robot.asay(random.choice(["Wanna play with me? It will cheer you up", "Lets play, It will improve you mood"]))
		else:
		   pepper_cmd.robot.asay("Great")
		   pepper_cmd.robot.asay(random.choice(["Would you like to play Tic-Tac-Toe Game with me?","Do you wanna"]))
		   
                if SIMULATION:
			if play:
			   subprocess.Popen('python $PEPPER_TOOLS_HOME/asr/human_say.py --sentence "yes"', shell=True)
			else:
			   subprocess.Popen('python $PEPPER_TOOLS_HOME/asr/human_say.py --sentence "no"', shell=True)
		   
		answer = pepper_cmd.robot.asr(yes_no,timeout)
		if answer not in ["yes", "sure", "yes please"]:  # Valid answer
	    	  if sad:
	    	    # trying to convince player if sad
		    pepper_cmd.robot.say("No, please play with me")
		    pepper_cmd.robot.say("Do you wanna play?")
		    if SIMULATION:
			    if play:
			       subprocess.Popen('python $PEPPER_TOOLS_HOME/asr/human_say.py --sentence "yes"', shell=True)
			    else:
			       subprocess.Popen('python $PEPPER_TOOLS_HOME/asr/human_say.py --sentence "no"', shell=True)
		    answer = pepper_cmd.robot.asr(yes_no,timeout)
		    if play:
		       user_play=True
		    else:
		       user_play=False
		    
	    	  else:
		    pepper_cmd.robot.say("Okay, see you next time")
		    user_play=False
		    print "********************PLAYER LEFT******************************"
	 
		else:
		   user_play=True
		   pepper_cmd.robot.run_behavior(random.choice(start_behave))
		   
	return user_play
 
 
def ask_game_type():

        global game_type
	pepper_cmd.robot.say("Please Choose you game type on the screen")
	ws_handler.send("event enter-profiling")
	while not the_bb.game_type:
	   pass
	game_type=the_bb.game_type # choosing type of game
        the_bb.game_type=None
        return game_type

def initialize_game(game_type):
        global game_plans
        global game
	if game_type == "4x":
	      game=tic4.Tic()
	      print("4x4 game is starting") 
	      
	else:
	      game=tic3.Tic()
	      with open('RA/game_plans_3x.json') as file:
                 game_plans = json.load(file)
                 print("3x3 game is starting") 
                        


 ###############################################################################################################################################################
 
begin() # connect to simulator with IP in PEPPER_IP env variable
pepper_cmd.robot.startSensorMonitor()
pepper_cmd.robot.normalPosture()

bname="animations/Stand/Waiting/Think_1"
anim2="animations/Stand/Gestures/ShowTablet_2"
#pepper_cmd.robot.my_asay(sent,anim)


#pepper_cmd.robot.dance()


the_bb = Blackboard()
the_webserver_thread = WebServerThread(the_bb)
the_webserver_thread.start()
#wait for connection
print "Reminder: open browser at 127.0.0.1:8888/web/index.html"
subprocess.Popen("xdg-open 'http://127.0.0.1:8888/web/index.html'", shell=True)

while not the_bb.the_handler:
    pass
ws_handler = the_bb.the_handler

pepper_player = 1
human_player = 2
game_type="3x" #Default game type

game_plans=None
rounds=2
sensor=[0,2]  #starting with backsonar
#sensor=[2,0]  #starting with frontsonar


introduction(False)
#wanna_play=True #debug
wanna_play=conversation(True)
if wanna_play:
	pepper_cmd.robot.say("Great!")
        game_type=ask_game_type()
        initialize_game(game_type)
        
	while wanna_play:
	    
	    #initialize board and play
	    try:
		game_over,winner = play_game(game,pepper_player, human_player,game_type)
	    except UserLeavingException as e:
		print "exception: ", e
		ws_handler.send("event interaction-end")
		#return
	    if rounds==1:
	       play_again=False
	    
            if game_over:
		    if winner == pepper_player:
		       print "WINNER IS: Pepper  "
		       pepper_cmd.robot.say(random.choice(["Well Played","Yeah! I won","It was hard to win"]))
		       pepper_cmd.robot.run_behavior(random.choice(pepper_win))
		    elif winner == human_player:
		       pepper_cmd.robot.say(random.choice(["Oh! you won ","You are good in this"]))
		       pepper_cmd.robot.run_behavior(random.choice(human_win))
		       print "WINNER IS: Human Player  "
		    elif winner == 0:
		       pepper_cmd.robot.say(random.choice(["Oh! you gave me a hard time","Huh? It's a draw..."]))
		       print "Game Draw  "
    
		    print "********************GAME END******************************"      
		    pepper_cmd.robot.say("Do you want to play again?")
		    if SIMULATION:
		            if play_again:
			       subprocess.Popen('python $PEPPER_TOOLS_HOME/asr/human_say.py --sentence "yes"', shell=True)
			       rounds-=1
			    else:
			       subprocess.Popen('python $PEPPER_TOOLS_HOME/asr/human_say.py --sentence "no"', shell=True)
		       
		    answer = pepper_cmd.robot.asr(yes_no,timeout)
		    if answer not in ["yes", "sure", "yes please"]:
		       pepper_cmd.robot.say("Okay, See you next time, lets shake hands")
		       # to be defined shake hand gesture
		       wanna_play=False
		      
		       
		       
		       
		    else:
		       pepper_cmd.robot.say("Do you want to change game type?")
		       
		       if SIMULATION:
			       if change_level_play_again:
				  subprocess.Popen('python $PEPPER_TOOLS_HOME/asr/human_say.py --sentence "yes"', shell=True)
			       else:
				  subprocess.Popen('python $PEPPER_TOOLS_HOME/asr/human_say.py --sentence "no"', shell=True)
		       answer = pepper_cmd.robot.asr(yes_no,timeout)
		       if answer not in ["yes", "sure", "yes please"]:
		          pass
		          
		       else:
		          game_type=ask_game_type()
                          initialize_game(game_type)
		          
		       pepper_cmd.robot.say("OK! Lets start the game")
		       wanna_play=True
	    else:
	        wanna_play=False
ws_handler.send("event interaction-end")
pepper_cmd.robot.normalPosture()
print "********************INTERACTION END******************************"		         
		          
		          
		          
		       
pepper_cmd.robot.stopSensorMonitor()
end()
sys.exit()
