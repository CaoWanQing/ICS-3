"""
Created on Sun Apr  5 00:00:32 2015

@author: zhengzhang
"""
from chat_utils import *
import json
import player 

class ClientSM:
    def __init__(self, s):
        self.state = S_OFFLINE
        self.peer = ''
        self.me = ''
        self.out_msg = ''
        self.s = s

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def set_myname(self, name):
        self.me = name

    def get_myname(self):
        return self.me

    def connect_to(self, peer):
        msg = json.dumps({"action":"connect", "target":peer})
        mysend(self.s, msg)
        response = json.loads(myrecv(self.s))
        if response["status"] == "success":
            self.peer = peer
            self.out_msg += 'You are connected with '+ self.peer + '\n'
            return (True)
        elif response["status"] == "busy":
            self.out_msg += 'User is busy. Please try again later\n'
        elif response["status"] == "self":
            self.out_msg += 'Cannot talk to yourself (sick)\n'
        else:
            self.out_msg += 'User is not online, try again later\n'
        return(False)

    def disconnect(self):
        msg = json.dumps({"action":"disconnect"})
        mysend(self.s, msg)
        self.out_msg += 'You are disconnected from ' + self.peer + '\n'
        self.peer = ''
    
    def blackjack_with(self, peer):
        #print("blackjack function get called!")

        msg = json.dumps({"action":"blackjack", "target":peer})
        mysend(self.s, msg)
        response = json.loads(myrecv(self.s))
        #print("response is ", response)
        if response["status"] == "self":
            self.out_msg += 'Cannot play blackjack with yourself. Find a peer!\n'
        elif response["status"] == "success":
            self.peer = peer
            #self.out_msg += 'You are now in game with '+ self.peer + '\n'
            return (True)
        elif response["status"] == "talking":
            self.out_msg += "The user is busy chatting. Find another peer!"
        else:
            self.out_msg += "User is not online, try again later\n"
        return(False) 
    
    def blackjack_disconnect(self):
        msg = json.dumps({"action":"bjdisconnect", "peer":self.peer})
        mysend(self.s, msg)
        self.out_msg += "You left the blackjack game\n"
        self.peer = ""

    def proc(self, my_msg, peer_msg):
        self.out_msg = ''
#==============================================================================
# Once logged in, do a few things: get peer listing, connect, search
# And, of course, if you are so bored, just go
# This is event handling instate "S_LOGGEDIN"
#==============================================================================
        if self.state == S_LOGGEDIN:
            # todo: can't deal with multiple lines yet
            if len(my_msg) > 0:

                if my_msg == 'q':
                    self.out_msg += 'See you next time!\n'
                    self.state = S_OFFLINE

                elif my_msg == 'time':
                    mysend(self.s, json.dumps({"action":"time"}))
                    time_in = json.loads(myrecv(self.s))["results"]
                    self.out_msg += "Time is: " + time_in

                elif my_msg == 'who':
                    mysend(self.s, json.dumps({"action":"list"}))
                    logged_in = json.loads(myrecv(self.s))["results"]
                    self.out_msg += 'Here are all the users in the system:\n'
                    self.out_msg += logged_in

                elif my_msg[0] == 'c':
                    peer = my_msg[1:]
                    peer = peer.strip()
                    if self.connect_to(peer) == True:
                        self.state = S_CHATTING
                        self.out_msg += 'Connect to ' + peer + '. Chat away!\n\n'
                        self.out_msg += '-----------------------------------\n'
                    else:
                        self.out_msg += 'Connection unsuccessful\n'

                elif my_msg[0] == '?':
                    term = my_msg[1:].strip()
                    mysend(self.s, json.dumps({"action":"search", "target":term}))
                    search_rslt = json.loads(myrecv(self.s))["results"].strip()
                    if (len(search_rslt)) > 0:
                        self.out_msg += search_rslt + '\n\n'
                    else:
                        self.out_msg += '\'' + term + '\'' + ' not found\n\n'

                elif my_msg[0] == 'p' and my_msg[1:].isdigit():
                    poem_idx = my_msg[1:].strip()
                    mysend(self.s, json.dumps({"action":"poem", "target":poem_idx}))
                    poem = json.loads(myrecv(self.s))["results"]
                    # print(poem)
                    if (len(poem) > 0):
                        self.out_msg += poem + '\n\n'
                    else:
                        self.out_msg += 'Sonnet ' + poem_idx + ' not found\n\n'

                elif my_msg[0] == 'g':
                    self.state = S_GAMBLING
                    gamble_choice = my_msg[1:].split()
                    mysend(self.s, json.dumps({"action": "gamble", "target": gamble_choice}))

                elif my_msg[0] == "b":
                    peer = my_msg[1:]
                    peer = peer.strip()
                    if self.blackjack_with(peer) == True:
                        self.state = S_BLACKJACK
                        self.out_msg += "You are now in game with " + peer + " . Start playing!\n"
                        self.out_msg += 'Welcome to BlackJack!\n'
                        self.out_msg += 'Both players will be dealt 2 cards each to start off\n'
                        self.out_msg += 'After that, please enter stay or hit when prompted\n'
                        self.out_msg += "Enter quit game if you want to leave the game\n"
                        self.out_msg += '-----------------------------------\n'
                        self.player = player.Player(self.me)
                        ACE_NUM = 100
                        self.out_msg += self.player.hit(ACE_NUM)
                        self.out_msg += self.player.hit(ACE_NUM)
                        self.out_msg += self.player.display_hand() + "\n"                        
                        self.out_msg += "Your current score is " + str(self.player.score) + "\n"
                        self.out_msg += "Please make a turn\n"
                        
                        #print(self.player.display_hand())
                        #self.out_msg += "display hand" + self.player.display_hand()        
                    else:
                        self.out_msg += 'blackjack request unsuccessful\n'
                else:
                    self.out_msg += menu

            if len(peer_msg) > 0:
                peer_msg = json.loads(peer_msg)
                if peer_msg["action"] == "connect":
                    self.peer = peer_msg["from"]
                    self.out_msg += 'Request from ' + self.peer + '\n'
                    self.out_msg += 'You are connected with ' + self.peer
                    self.out_msg += '. Chat away!\n\n'
                    self.out_msg += '------------------------------------\n'
                    self.state = S_CHATTING
                
                elif peer_msg["action"] == "blackjack":
                    self.peer = peer_msg["from"]
                    #self.out_msg += "Blackjack request from " + self.peer + "\n"
                    #self.out_msg += "Reply yes or no to the request" + "\n"
                    self.out_msg += 'Blackjack request from ' + self.peer + '\n'
                    self.out_msg += 'You are now in game with ' + self.peer + "\n"
                    self.out_msg += 'Welcome to BlackJack!\n'
                    self.out_msg += 'Both players will be dealt 2 cards each to start off\n'
                    self.out_msg += 'After that, please enter stay or hit when prompted\n'
                    self.out_msg += "Enter quit game if you want to leave the game\n"                    
                    self.out_msg += 'Start playing!\n\n'
                    self.out_msg += '------------------------------------\n'
                    self.player = player.Player(self.me)
                    ACE_NUM = 100
                    self.out_msg += self.player.hit(ACE_NUM)
                    self.out_msg += self.player.hit(ACE_NUM)
                    self.out_msg += self.player.display_hand() + "\n"
                    self.out_msg += "Your current score is " + str(self.player.score) + "\n"
                    self.out_msg += "Please wait for " + self.peer + "'s move\n"
                    self.state = S_BLACKJACK
                    #score_reply = json.loads(myrecv(self.s))
                    #score = score_reply["score"]
                    #self.out_msg += self.peer + " chooses to " + score_reply["move"] + "\n" 
                    #self.out_msg += self.peer + "'s current score is " + score + "\n"



#==============================================================================
# Start chatting, 'bye' for quit
# This is event handling instate "S_CHATTING"
#==============================================================================
        elif self.state == S_CHATTING:
            if len(my_msg) > 0:     # my stuff going out
                mysend(self.s, json.dumps({"action":"exchange", "from":"[" + self.me + "]", "message":my_msg}))
                if my_msg == 'bye':
                    self.disconnect()
                    self.state = S_LOGGEDIN
                    self.peer = ''
            if len(peer_msg) > 0:    # peer's stuff, coming in
                peer_msg = json.loads(peer_msg)
                if peer_msg["action"] == "connect":
                    self.out_msg += "(" + peer_msg["from"] + " joined)\n"
                elif peer_msg["action"] == "disconnect":
                    self.state = S_LOGGEDIN
                else:
                    self.out_msg += peer_msg["from"] + peer_msg["message"]


            # Display the menu again
            if self.state == S_LOGGEDIN:
                self.out_msg += menu
#==============================================================================
# Start game, 'quit game' for quit
# This is event handling instate "S_BLACKJACK"
#==============================================================================
        elif self.state == S_BLACKJACK:
            ACE_NUM = 100
            if len(my_msg) > 0:
                if my_msg == "quit game":
                    self.blackjack_disconnect()
                    self.state = S_LOGGEDIN
                    self.peer = ""
                elif my_msg == "hit":
                    self.out_msg += self.player.hit(ACE_NUM)
                    self.out_msg += self.player.display_hand() + "\n"
                    self.out_msg += "Your current score is " + str(self.player.score) + "\n"
                    if self.player.peer_active == True and self.player.score < 21:
                        self.out_msg += "Please wait for the other player's move\n"
                    if self.player.score > 21:
                        self.out_msg += "Unfortunately you have lost the game. See you next time\n"
                        self.state = S_LOGGEDIN
                        self.out_msg += menu
                elif my_msg == "stay":
                    self.out_msg += self.player.stay()
                    self.player.active = False
                    if self.player.peer_active == False:
                        #self.out_msg += "Game result in my_msg part get called!"
                        self.out_msg += "------------------GAME RESULT------------------\n"
                        self.out_msg += "Both players have completed playing.\n"
                        self.out_msg += "Your score is " + str(self.player.score) + "\n"
                        self.out_msg += self.peer + "'s score is " + self.player.peer_score + "\n"
                        if int(self.player.score) > int(self.player.peer_score):
                            self.out_msg += "Congratulations! You win!\n"
                            self.out_msg += menu
                        elif int(self.player.score) == int(self.player.peer_score):
                            self.out_msg += "The game is tied.\n"
                            self.out_msg += menu
                        else:
                            self.out_msg += "Unfortunately you've lost the game.\n"
                            self.out_msg += menu
                        self.state = S_LOGGEDIN
                mysend(self.s, json.dumps({"action":"sendscore", "score":str(self.player.score), 
                            "move":my_msg, "target":self.peer, "active": self.player.active}))

                
            if len(peer_msg) > 0:
                peer_msg = json.loads(peer_msg)
                if peer_msg["action"] == "bjdisconnect":
                    self.out_msg += "The other player left the game. Game over.\n"
                    self.state = S_LOGGEDIN
                if peer_msg["action"] == "sendscore":
                    peer_score = peer_msg["score"]
                    self.player.peer_score = peer_score
                    self.player.peer_active = peer_msg["active"]
                    self.out_msg += self.peer + "'s score is " + peer_score + "\n"                
                    if int(peer_score) > 21:
                        self.out_msg += "The other player is busted. You win!\n"
                        who_wins = self.me
                        mysend(self.s, json.dumps({"action": "get_result", "target": who_wins}))
                        self.out_msg += menu
                        self.state = S_LOGGEDIN
                    elif self.player.active == True:
                        self.out_msg += "Please make your move\n"
                    elif self.player.active == False and self.player.peer_active == False:
                        self.out_msg += "------------------GAME RESULT------------------\n"
                        self.out_msg += "Both players have completed playing.\n"
                        self.out_msg += "Your score is " + str(self.player.score) + "\n"
                        self.out_msg += self.peer + "'s score is " + self.player.peer_score + "\n"
                        if int(self.player.score) > int(self.player.peer_score):
                            self.out_msg += "Congratulations! You win!\n"
                            who_wins = self.me
                            mysend(self.s, json.dumps({"action": "get_result", "target": who_wins}))
                        elif int(self.player.score) == int(self.player.peer_score):
                            self.out_msg += "The game is tied.\n"
                        else:
                            self.out_msg += "Unfortunately you've lost the game.\n"    
                        self.out_msg += menu
                        self.state = S_LOGGEDIN
# ==============================================================================
# gamble result
# ==============================================================================
        elif self.state == S_GAMBLING:
            if len(peer_msg) > 0:
                peer_msg = json.loads(peer_msg)
                if peer_msg["action"] == "gamble":
                    self.out_msg += "You " + peer_msg["status"] + "! You now have " + str(peer_msg["money"]) + "kuai \n"

#==============================================================================
# invalid state
#==============================================================================
        else:
            self.out_msg += 'How did you wind up here??\n'
            print_state(self.state)

        return self.out_msg
