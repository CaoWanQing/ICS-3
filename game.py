  import sys
#from player import *
import player

def play():
	
	ACE_NUM = 100
	game_over = False
	p1_turn = True
	
	#creating 2 player objects
	player1 = player.Player('Player 1')
	player2 = player.Player('Player 2')
	
	#print out  rules
	print('\n\n')
	print('Welcome to BlackJack!')
	print('Both players will be dealt 2 cards each to start off')
	print('After that, please enter stay or hit when prompted')
	print('\n\n')

	#selecting which cards the 2 players start off with
	#I don't re-select the cards if the score is 21 here itself
	#if the score here is 21, you must enter stay on the next turn to win the game
	
	print(player1.name)
	player1.hit(ACE_NUM)
	player1.hit(ACE_NUM)
	print('\n\n')
	print(player2.name)
	player2.hit(ACE_NUM)
	player2.hit(ACE_NUM)
	print('\n\n')
	
	#continue game while there is no winner
	while(not game_over):
		
		'''
		determining whose turn it is based on
		alternating turns and who is still playing the game
		'''

		if player1.active and player2.active:
			if p1_turn:
				current_player = player1
			if not p1_turn:
				current_player = player2
		elif player1.active and not player2.active:
			current_player = player1
		elif not player1.active and player2.active:
			current_player = player2
		else:
			#This is the case where both players have selected stay
			if player1.score > player2.score:
				print('Congratulations ' + player1.name + '! You are the winner!!')
				game_over = not game_over
				continue
			elif player2.score > player1.score:
				print('Congratulations ' + player2.name + '! You are the winner!!')
				game_over = not game_over
				continue
			else:
				print('The game is tied.')
				game_over = not game_over
				continue

		#tell the player their hand and score before their turn
		print(current_player.name)
		current_player.display_hand()
		print('Your score is currently: ' + str(current_player.score))
		print('Please make a turn')
		
		done = False
		
		#ask user for choice of hit and stay and execute respective function
		while(not done):
			answer = input()
			if answer == 'hit':
				current_player.hit(ACE_NUM)
				done = True
			elif answer == 'stay':
				current_player.stay()
				done = True
			else:
				print('Please enter either hit or stay')
	
		#handling if game ends by conclusion of this turn
		print('\n\n')
		if current_player.score == 21:
			print('Congratulations ' + current_player.name + '! You are the winner!!')
			game_over = not game_over
		if current_player.score > 21:
			print(current_player.name + ', unfortunately you have lost the game.')
			game_over = not game_over
			
		p1_turn = not p1_turn

play()