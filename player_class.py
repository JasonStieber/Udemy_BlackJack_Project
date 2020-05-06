# create player class
class player:
    
    def __init__ (self, name, buyin):
        self.name = name
        self.balance = buyin
        self.hands_played = 0
        self.hands_won = 0
        self.bet_history = []
        self.hands_pushed = 0
        self.current_hand = []
        # bet hisotry is a varable to stores win/loss and bet amount

    def __str__(self):
        return f'{self.name} has ${self.balance} remaining'

    def chk_bal(self):
        return self.balance

    def add_funds(self, amount):
        self.balance += amount

    def withdraw_funds(self, amount):
        if amount > self.balance:
            # didn't work
            return False
        else:
            self.balance -= amount
            return True

    def hand_result(self, amount, winnings):
        self.hands_played += 1
        if amount < winnings:
            self.hands_won += 1
        elif amount == winnings:
            self.hands_pushed += 1
        else:
            pass
        self.bet_history.append((amount, winnings - amount))
        self.add_funds(winnings)

    # name / buying amount
