# create deck
"""DOCSTRING: Creat a black jack game from scratch"""
import random
import time
import player_class
CARDS = ("A", "K", 'Q', 'J', 'T', 9, 8, 7, 6, 5, 4, 3, 2)
SUITS = ('\u2663', '\u2660', '\u2665', '\u2666')
current_shoe = []
dealers_hand = []
last_hand = False
reveal_dealer_hand = False


def create_shoe(num_of_decks):
	'''
	DOCSTRING: Create a shuffled shoe of any number of decks
	INPUT: an int > = 1
	OUTPUT: no output this function changes the global variable current_shoe
	'''
	global current_shoe
	global cut_card
	current_shoe = []
	for card in CARDS:
		current_shoe += ([(card, suit) for suit in SUITS])
	current_shoe *= num_of_decks
	random.shuffle(current_shoe)
	# create cut card to stop the game before cards run out
	cut_pos = int(round(len(current_shoe) * .15, 0))
	current_shoe[cut_pos] = (False, 'Joker')

#display current hand
def show_current_hand(player):
	print('\n'*100)
	print("Dealer Hand")
	if reveal_dealer_hand:
		print_hand(dealers_hand)
	else:
		print_dealer_hidden_hand(dealers_hand)
	print('\n'*5)
	print_hand(player.current_hand)
	hand_total = count_hand(player.current_hand)
	if hand_total[1]:
		print(f"You have {hand_total[0]} or {hand_total[0] + 10}")
	else:
		print(f"You have a total of {hand_total[0]}")

def chk_black_jack(hand):
	"""DOCSTRING: reutrn true if the hand passed in is a black jack
	INPUT: a list of tuples cards and suits
	OUTPUT: a bool true if and only if the hand is a black Jack
	"""
	hand_total = count_hand(hand)
	return len(hand) == 2 and hand_total[0] == 11 and hand_total[1] == True

# count hand
def count_hand(hand):
	"""
	DOCSTRING: this function takes in a hand of cards and counts them
	INPUT: takes in a list of tuples of cards, (num, suit)
	OUTPUT: returns a tuple of the total and if it could also be 10 - the total
	"""
	count = 0
	has_ace = False
	for card in hand:
		if type(card[0]) == str and card[0] != "A":
			count += 10
		elif card[0] == 'A':
			count += 1
			has_ace = True
		else:
			count += card[0]
	if has_ace and count <= 11:
		return (count, True)
	else:
		return (count, False)

def draw_card(hand):
	"""
	DOCSTRING: check for the final card in the shoe if it exists set global variable last hadn to true
	INPUT: a list hand
	OUTPUT: N/A
	"""
	global last_hand
	next_card = current_shoe.pop()
	if next_card[0]:
		hand.append(next_card)
	else:
		hand.append(current_shoe.pop())
		last_hand = True
	return count_hand(hand)


# player plays hand until stays
def play_hand(player):
	"""
	DOCSTRING: Player plays BJ until they bust or stay
	INPUT: a player class object
	OUTPUT: none
	"""
	stay = False
	while not stay:
		show_current_hand(player)
		stay = False
		reveal_dealer_hand = False
		action = ''
		while True:
			action = input("Would you like to Hit (H), or Stay (S): ")
			action = action.capitalize()
			if action == "H" or action == "S" or action == "Hit" or action == "Stay":
				break
			else:
				print("Not a valid command please try again ")
		if action == "S" or action == "Stay":
			show_current_hand(player)
			reveal_dealer_hand = True
			stay = True
		elif action == "H" or action == "Hit":
			# busted
			if draw_card(player.current_hand)[0] > 21:
				show_current_hand(player)
				print("You busted\n")
				reveal_dealer_hand = True
				return "Bust"

		else:
			raise Exception("not hit or stay")

def does_player_wins(dealer_hand, player_hand):
	"""DOCSTRING: compaires two hands retures ture if player wins false if dealer wins 'Push' if a push"
	INPUT: two hands list of tuples [(card, suit)]
	OUTPUT: Ture if player wins False if dealer wins 'Push if push'
	"""
	player_count = count_hand(player_hand)
	if player_count[1]:
		player_count = player_count[0]+10
	else:
		player_count = player_count[0]
	dealer_count = count_hand(dealer_hand)
	if dealer_count[1]:
		dealer_count = dealer_count[0] + 10
	else:
		dealer_count = dealer_count[0]
	#check for a push
	if dealer_count == player_count:
		return "Push"
	else:
		return player_count > dealer_count

# deal function
def deal(*args):
	global dealers_hand
	global current_shoe
	global last_hand
	dealers_hand = []
	for player in args:
		player.current_hand = []
	for i in range(0, 2):
		for player in args:
			draw_card(player.current_hand)
		draw_card(dealers_hand)

# rebuy function

# print card
def print_hand(hand):
	nums = ''
	suits = ''
	for card in hand:
		nums += f"| {card[0]} | "
		suits += f"| {card[1]} | "
	print("----- "*len(hand) + "\n" + nums + "\n"+ suits + "\n" + "----- "*len(hand))

def print_dealer_hidden_hand(hand):
	print("----- "*2 + "\n" + f"| ? | | {hand[1][0]} | " + "\n"+ f"| ? | | {hand[1][1]} | " + "\n" + "----- "*len(hand))



def run_game():
	global reveal_dealer_hand
	global last_hand
	name = input("Who would like to play Blackjack? ")
	while True:
		try:
			buyin = int(input("And how much would you like to play for? "))
			break
		except:
			print("That is not a valid buyin please enter only full dolar amounts. ")
	new_player = player_class.player(name, buyin)
	while True:
		try:
			decks = int(input("How many decks will be in this shoe 1-10: "))
			if decks > 10 or decks < 1:
				print("Invalid number of decks, please try again: ")
			else: 
				break
		except:
			print("That is not a valid number, try again ")
	#start playing
	while True:
		play_again = ""
		if last_hand:
			play_again = input("The shoe is over would you like to play another shoe? Y, N: ")
			if play_again.lower() == "n" or play_again.lower() == 'no':
				break
		last_hand = False
		while not last_hand:
			print("shuffling shoe......")
			create_shoe(decks)
			bet = 0
			while not last_hand:
				print(f"the shoe has {len(current_shoe)} cards left in it")
				reveal_dealer_hand = False
				#deal begin the shoe
				while True:
					try:
						bet = int(input(f"How much would you like to bet {new_player.name}? You have {new_player.balance} remaining "))
						while not new_player.withdraw_funds(bet):
							print("You do not have that balance avilable: ")
							while True:
								try:
									bet = int(input(f"How much would you like to bet {new_player.name}? You have {new_player.balance} remaining "))
								except:
									print("that isn't a valid bet: ")
								else:
									break
						# stop player from being able to pull out more then they have	
					except:
						print("that isn't a valid bet: ")
					else:
						break
				deal(new_player)
				show_current_hand(new_player)
				#check for black jacks
				if chk_black_jack(new_player.current_hand) and not chk_black_jack(dealers_hand):
					print("Winner winner Chicken Dinner!")
					new_player.hand_result(bet, bet*2.5)
					reveal_dealer_hand = True
					show_current_hand(new_player)
				elif chk_black_jack(new_player.current_hand):
					new_player.hand_result(bet, bet)
					reveal_dealer_hand = True
					show_current_hand(new_player)
				elif chk_black_jack(dealers_hand):
					reveal_dealer_hand = True
					new_player.hand_result(bet, 0)
					show_current_hand(new_player)
				# this if refers to if a player doesn't bust, then the dealer gets a turn
				elif play_hand(new_player) == "Bust":
					reveal_dealer_hand = True
					show_current_hand(new_player)
				else:
					# run out dealer hand
					while True:
						show_current_hand(new_player)
						dealer_total = count_hand(dealers_hand)
						# if dealer has a staying hand
						# dealer busts
						if dealer_total[0] > 21:
							# dealer busts pay out player and anounce win and ask to play again
							reveal_dealer_hand = True
							show_current_hand(new_player)
							print(f"Dealer busts with {dealer_total[0]}, you win! ")
							new_player.hand_result(bet,bet*2)
							break
						# dealer has a hand to stay
						elif dealer_total[0] >= 17 or (dealer_total[0] > 7 and dealer_total[1] == True):
							# compare hands pay out winners or pushes
							if does_player_wins(dealers_hand, new_player.current_hand) == "Push":
								new_player.hand_result(bet, bet)
								reveal_dealer_hand = True
								show_current_hand(new_player)
								print("You Push ")
							elif does_player_wins(dealers_hand, new_player.current_hand):
								new_player.hand_result(bet, bet*2)
								reveal_dealer_hand = True
								show_current_hand(new_player)
								print("You Win!!!! ")
							else:
								new_player.hand_result(bet, 0)
								reveal_dealer_hand = True
								show_current_hand(new_player)
								print("Dealer wins")
							break

						# dealer stays
						else:
							#dealer keeps hitting
							draw_card(dealers_hand)
							time.sleep(0.5)

# check for dealer blackjack function

# run game 

run_game()
