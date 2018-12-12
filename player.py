import random

class Player():
	ACE_NUM = 100
	deck = [i for i in range(1,14)]
	frequency_deck = {'2': 4, '3':4, '4':4, '5':4, '6':4, '7':4, '8':4, '9':4, '10':4, \
						'ace':4, 'jack':4, 'queen':4, 'king':4} 
	#frequency_deck maps cards to the number of those left in the deck
	
	
	def __init__(self, name):
		self.name = name
		self.hand = [] #list of cards in hand as strings
		self.value_hand = [] #list of values of cards in hand
		self.score = 0
		self.peer_score = 0
		self.active = True
		self.peer_active = True
	
	#prints out the player's hand
	def display_hand(self):
		return('Your hand is currently: ' + str(self.hand))
	
	
	#what to do if user wants to hit
	def hit(self, ACE_NUM):
		card = random.choice(Player.deck)
		value = 0

		#Displaying the card that has been dealt
		temp_str = ''
		if card == 13:
			temp_str = 'king'
			value = 10
		elif card == 12:
			temp_str = 'queen'
			value = 10
		elif card == 11:
			temp_str = 'jack'
			value = 10
		elif card == 1:
			temp_str = 'ace'
			value = ACE_NUM #placeholder for ace
		else:
			temp_str = str(card)
			value = card
		msg = 'You have been dealt a ' + temp_str +"\n"
		
		#handling if all cards of certain type have been dealt from hand
		Player.frequency_deck[temp_str] -= 1
		if Player.frequency_deck[temp_str] == 0:
			del Player.frequency_deck[temp_str]
			Player.deck.remove(card)
		
		#adding to the hand and optimizing the value
		self.hand.append(temp_str)
		self.value_hand.append(value)
		self.deal_with_ace(ACE_NUM)
		return msg
	
	#what to do if user wants to stay
	def stay(self):
		msg = 'You have completed playing' + "\n"
		msg += 'Your current hand is ' + str(self.hand) + "\n"
		msg += 'Your current score is ' + str(self.score) + "\n"
		self.active = False
		return msg
	
	#algorithm to optimize the use of the ace card(s) in the user's hand
	def deal_with_ace(self,ACE_NUM):
		#print("optimize function get called!")
		counter = 0
		for item in self.value_hand:
			if item == ACE_NUM:
				counter += 1
		
		if ACE_NUM in self.value_hand:
			#aces present in hand
			i = 0
			self.score = sum(self.value_hand) - (ACE_NUM * counter)

			#accounting for fact that there may be multiple aces in hand
			while (i < counter):
				add_eleven = self.score + 11
				add_one= self.score + 1

				if add_one > 21:
					self.score = add_one
				elif add_one < 21 and add_eleven > 21:
					self.score = add_one
				else:
					option1 = 21 - add_eleven
					option2 = 21 - add_one
					if option1 < option2:
						self.score = add_eleven
					else:
						self.score = add_one
				i += 1
		else:
			#if no aces in hand
			self.score = sum(self.value_hand)