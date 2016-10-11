# coding: utf-8

import random
from titlecase import titlecase
import time
import re
import os
from operator import itemgetter
from sopel.module import commands, example


# Enter the channel in which you want the game to run. Include the #.
CHANNEL = ''


def setup(bot):
    """Force a reload of the cards whenever this module is reloaded."""
    load_cards()


def load_cards():
    """Grab white and black cards from text files."""
    global white, black
    whitefile = os.path.join(os.path.dirname(__file__), 'cah-white-cards.txt')
    blackfile = os.path.join(os.path.dirname(__file__), 'cah-black-cards.txt')
    with open(whitefile, 'r', encoding='utf-8') as f:
        white = tuple(x for x in f.read().splitlines() if not x.startswith('#'))
    with open(blackfile, 'r', encoding='utf-8') as f:
        black = tuple(x for x in f.read().splitlines() if not x.startswith('#'))


def fill_black(card, whites=None):
    """Helper function that fills blanks in black cards with appropriate white cards."""
    whiter = iter(whites) if whites else iter([])
    fragments = re.split('(_[CTAS]?)', card)
    for i, fragment in enumerate(fragments):
        if fragment.startswith('_'):
            fragments[i] = transform_white(next(whiter, random.choice(white)), fragment[1:])
    return "".join(fragments)


def transform_white(whitecard, modifier):
    """Helper function that takes in a white card and type. Output is the modified text."""
    if modifier is 'C':  # Capitalizes the first letter
        return whitecard[0].capitalize() + whitecard[1:]
    elif modifier is 'T':  # Capitalizes the First Letter of Each Word
        return titlecase(whitecard)
    elif modifier is 'A':  # CAPITALIZES ALL LETTERS OH MY GOD
        return whitecard.upper()
    elif modifier is 'S':  # lowercaseandspacelesswithoutpunctuation
        return re.sub("\W", "", whitecard).lower()
    else:
        return whitecard


class Hand(object):
    def __init__(self):
        self.cards = []

    def draw_cards(self):
        """Draw cards up to the full hand size."""
        for each in range(humanity.cards_per_player - len(self.cards)):
            self.cards.append(humanity.whitedeck.pop())

    def __str__(self):
        """Display the hand of cards, assigning each a numerical value for ease of playing."""
        prettycards = ''
        uglycards = list(enumerate(self.cards, 1))
        # Make the cards display nice and purdy.
        for pair in uglycards:
            prettycards += "(%s, %s), " % (str(pair[0]), pair[1])
        # Trim trailing comma and space
        return prettycards[:-2]
        
    def play_card(self, bot, trigger):
        """trigger is the player name as a string and a list of integers."""
        cards_to_submit = []
        try:
            somecards = [int(s) for s in trigger.group(2).split()]
        except ValueError:
            bot.msg(CHANNEL, "Invalid card.")
            return
        # Exclude card czar from submitting white cards.
        if trigger.nick == humanity.playerOrder[humanity.currentPlayer]:
            bot.msg(CHANNEL, "You are the card czar.")
        # Prevent submitting cards more than once.
        elif humanity.submittedCards[trigger.nick]:
            bot.msg(CHANNEL, "You have already submitted cards this round.")
        # Ensure number of cards matches number of blanks.
        elif len(somecards) == humanity.current_black_card.count('_'):
            # Add the chosen cards to the list of submitted cards
            for each in somecards:
                try:
                    cards_to_submit.append(self.cards[each-1])
                except IndexError:
                    bot.msg(CHANNEL, "Invalid card.")
                    return
            # Remove the chosen cards from the list, in descending numerical order
            for each in sorted(somecards, reverse=True):
                self.cards.pop(each-1)
            humanity.add_card(bot, trigger.nick, cards_to_submit)
        else:
            bot.msg(CHANNEL, "Incorrect number of cards.")


class Humanity(object):
    def __init__(self):
        self.whitedeck = []
        self.blackdeck = []
        self.players = {}
        self.playerOrder = []
        self.playerScores = {}
        self.hands = []
        self.game_on = False
        self.started = False
        self.cards_per_player = 7
        self.winning_score = 3  # Default score for victory
        self.cards()
        self.numplayers = 0
        self.currentPlayer = 0
        self.submittedCards = {}
        self.Rando = False
        self.allowPlaying = False
        self.allowVoting = False
        self.advance = False
        self.stop_game = False
    
    def game_open(self, bot, starter, trigger):
        """Open the game for other players to join, and assign the starter a hand and position in the order."""
        if self.game_on:
            bot.msg(CHANNEL, "A game has already been started. Use .cahjoin to join it.")
        else:
            self.game_on = starter
            self.players[starter] = Hand()
            self.playerOrder.append(starter)
            self.playerScores[starter] = 0
            bot.msg(CHANNEL, "{} has started a new game! .cahjoin to join. Use .rando to invite Rando to the party, "
                             "and .cahstart to begin the game.".format(starter))
            if trigger.group(2):
                if int(trigger.group(2)) in range(3,9):
                    self.winning_score = int(trigger.group(2))
                else:
                    return
            bot.msg(CHANNEL, "The game will end at {} points.".format(str(self.winning_score)))
        
    def cahjoin(self, bot, trigger):
        """Add a player to the game, assigning them a hand object and position in the order list."""
        if not self.game_on:
            bot.msg(CHANNEL, "There is no game in progress. Use .cah to begin a new game.")
        elif trigger.nick not in self.players:
            self.players[trigger.nick] = Hand()
            self.playerOrder.append(trigger.nick)
            self.playerScores[trigger.nick] = 0
            bot.msg(CHANNEL, "{} has joined the game.".format(trigger.nick))
        else:
            bot.msg(CHANNEL, "You are already in the game.")
        
    def hand(self):
        for hand in self.players.values():
            hand.draw_cards()

    def rando_on(self, bot):
        """Set Rando to True and alert everyone to his arrival."""
        if self.game_on and not self.Rando:
            self.Rando = True
            self.playerScores["Rando Cardrissian"] = 0
            bot.msg(CHANNEL, "Hello, what have we here? Rando Cardrissian has joined the game!")
        elif self.Rando:
            bot.msg(CHANNEL, "Rando's already here, baby!")
        elif not self.game_on:
            bot.msg(CHANNEL, "The game hasn't started.")
    
    def cards(self):
        """Create the decks of cards for play and shuffle them."""
        global black, white
        self.whitedeck.extend(white)
        random.shuffle(self.whitedeck)
        self.blackdeck.extend(black)
        random.shuffle(self.blackdeck)
            
    def get_card(self, cardtype):
        """Return and remove the top card from a deck."""
        return cardtype.pop()
        
    def new_round(self, bot, trigger):
        """Begin a new round, draw and display a new black card."""
        # Do not start a new round if the game has been stopped.
        if not self.game_on:
            return
        self.started = True
        # Reset the dictionary of cards submitted by the players
        self.submittedCards = {}
        # Refresh everyone's hand with the correct number of cards
        self.hand()
        # Make an empty list for each player, in a submitted-card dictionary
        for each in self.players:
            self.submittedCards[each] = []
        # Draw and display the black card for the round
        self.current_black_card = self.get_card(self.blackdeck)
        bot.msg(CHANNEL, self.current_black_card)
        bot.msg(CHANNEL, "The card czar for this round is {}. Everyone else, please .cahplay a card or cards in the "
                         "order you wish them to be used. Example: .cahplay 1"
                .format(self.playerOrder[self.currentPlayer]))
        for each in self.players:
            if each != self.playerOrder[self.currentPlayer]:
                bot.notice(self.players[each].__str__(), each)
        # Allow cards to be submitted
        self.allowPlaying = True
        # Submit a Rando card if he is playing
        if self.Rando:
            self.rando_play(bot)

    def get_numplayers(self, bot):
        """Return the number of players, including Rando if he has joined."""
        self.numplayers = len(self.players) - 1
        if self.Rando:
            self.numplayers += 1
        return self.numplayers
        
    def rando_play(self, bot):
        """Play random white card(s) for Rando."""
        randocards = []
        self.submittedCards["Rando Cardrissian"] = []
        for each in range(self.current_black_card.count('_')):
            randocards.append(self.get_card(self.whitedeck))
        self.add_card(bot, "Rando Cardrissian", randocards)
        
    def add_card(self, bot, name, playedcards):
        """Plays a card or cards matching the number of blanks in the black card. Cards trigger is a list."""
        for each in playedcards:
            self.submittedCards[name].append(each)
        bot.notice("Card(s) submitted.", name)
        # Move to the voting round once all players have submitted cards
        if len({k: v for k, v in self.submittedCards.items() if v}) == self.get_numplayers(bot):
            self.czar_round(bot)

    def czar_round(self, bot):
        """Display the submitted cards for the czar to vote on."""
        self.allowPlaying = False
        # Re-display black card
        bot.msg(CHANNEL, self.current_black_card)
        # Display enumerated entries
        self.cardstovote = {k: v for k, v in self.submittedCards.items() if v}
        self.cardlist = list(enumerate(self.cardstovote.values(), 1))
        bot.msg(CHANNEL, "The entries are: {}".format(self.pretty_card_list(bot, self.cardlist)))
        self.allowVoting = True
        bot.msg(CHANNEL, self.playerOrder[self.currentPlayer] + ", please .cahvote for the entry you like most")
        
    def pretty_card_list(self, bot, cards):
        """Make the cardlist display nice and purdy."""
        prettycards = ''
        for pair in cards:
            temppretty = ''
            for each in pair[1]:
                temppretty += each + " | "
            prettycards += "(\x02%s\x0F, %s), " % (str(pair[0]), temppretty[:-3])
        # Trim trailing comma
        return prettycards[:-2]
    
    def czarVote(self, bot, trigger):
        """Select the voted card and send it to the end of the round."""
        if self.allowVoting:
            try:
                if int(trigger.group(2)) in range(1,len(self.cardlist)+1):
                    voted = self.cardlist[int(trigger.group(2))-1][1]
                    for name, cards in self.cardstovote.items():
                        if cards == voted:
                            # Send winning card(s) to end of round
                            self.roundEnd(bot, name, voted)
                else:
                    bot.msg(CHANNEL, "That is not a valid choice.")
            except ValueError:
                bot.msg(CHANNEL, "That is not a valid choice.")
                return
        else:
            bot.msg(CHANNEL, "It is not time to vote.")

    def roundEnd(self, bot, name, winner):
        """The card czar chooses a winner, and the black card is re-displayed with the winning white cards
        replacing the blanks. A point is assigned to the winner.
        """
        bot.msg(CHANNEL, "{} wins with: {}".format(name, fill_black(self.current_black_card, winner)))
        # Maybe save winning card combo to a file?
        self.playerScores[name] += 1
        self.get_scores(bot)
        self.allowVoting = False
        self.cardstovote = {}
        self.cardlist = []
        if self.playerScores[name] >= self.winning_score:
            bot.msg(CHANNEL, "Congratulations to {}! They won the game with {} points!"
                    .format(name, str(self.playerScores[name])))
            # Save scores to file?
            self.game_on = False
        else:
            bot.msg(CHANNEL, "A new round will begin in 15 seconds.")
            time.sleep(15)
            self.playerOrder.append(self.playerOrder.pop(0))
            self.new_round(bot, None)

    def get_scores(self, bot):
        """Return the scoreboard for the current game."""
        if len(self.playerScores) == 0:
            return
        else:
            # Slightly better score display
            uglyscores = [(k[0:], v) for k, v in self.playerScores.items()]
            uglyscores = sorted(uglyscores, key=itemgetter(1, 0), reverse=True)
            prettyscores = "; ".join((p[0] + ": " + str(p[1])) for p in uglyscores)
            bot.msg(CHANNEL, prettyscores)

    def cahleave(self, bot, trigger):
        """Allow a player to leave a game in progress. Probably buggy."""
        if self.game_on and trigger.nick in self.players:
            del self.players[trigger.nick]
            self.playerOrder.remove(trigger.nick)
            bot.msg(CHANNEL, trigger.nick + " has left the game.")
        elif not self.game_on:
            bot.msg(CHANNEL, "There is no game in progress.")
        elif trigger.nick not in self.players:
            bot.msg(CHANNEL, "You aren't even playing!")

    def cahstop(self, bot, trigger):
        """Stop a game in progress."""
        global humanity
        # Allow the creator to stop a game in progress, after confirmation
        if self.stop_game and trigger.nick == self.game_on:
            bot.msg(CHANNEL, "Game stopped.")
            self.game_on = False
            humanity = Humanity()
        else:
            # Confirm if creator wants to stop the game
            if trigger.nick == self.game_on:
                self.stop_game = True
                bot.msg(CHANNEL, "Are you sure you wish to stop the game? If so, type .cahstop again.")
            else:
                bot.msg(CHANNEL, "You did not start the game.")


load_cards()
humanity = Humanity()

@commands('cah')
@example('.cah or .cah 5')
def cah(bot, trigger):
    if not humanity.game_on:
        humanity.__init__()
    humanity.game_open(bot, trigger.nick, trigger)


@commands('cahjoin')
def cahjoin(bot, trigger):
    humanity.cahjoin(bot, trigger)


@commands('cahplay', 'cp')
@example('.cp 1 or .cp 1 5')
def cahplay(bot, trigger):
    if humanity.game_on:
        humanity.players[trigger.nick].play_card(bot, trigger)


@commands('cahvote', 'cv')
@example('.cv 2')
def cahvote(bot, trigger):
    if humanity.game_on:
        if trigger.nick == humanity.playerOrder[humanity.currentPlayer]:
            humanity.czarVote(bot, trigger)


@commands('cahstart')
def cahstart(bot, trigger):
    if humanity.game_on:
        if not humanity.started and trigger.nick == humanity.game_on:
            humanity.new_round(bot, trigger)


@commands('cahscores')
def cahscores(bot, trigger):
    humanity.get_scores(bot)


@commands('rando')
def rando(bot, trigger):
    humanity.rando_on(bot)


@commands('cahleave')
def cahleave(bot, trigger):
    if humanity.game_on:
        humanity.cahleave(bot, trigger)


@commands('cahstop')
def cahstop(bot, trigger):
    if humanity.game_on:
        humanity.cahstop(bot, trigger)
