# This Python file uses the following encoding: utf-8

from titlecase import titlecase
import random
from sopel.module import commands, example
import re
import os


@commands('cahload')
def loadcards(bot, trigger):
    """Reload the cards from their text files."""
    load_cards()
    bot.say("Reloaded %d black cards and %d white cards." % (len(black), len(white)))


@commands('cardcount')
def cardcount(bot, trigger):
    """Return the number of white and black cards in the decks."""
    bot.say("There are %d black cards and %d white cards." % (len(black), len(white)))


@commands('hate')
def _handle_hate(bot, trigger):
    """Return a random, valid combination of cards."""
    bot.say(fill_black(random.choice(black)))


@commands('bc')
@example('.bc My new book is titled "_T"')
def _handle_bc(bot, trigger):
    """Make your own Cards Against Humanity black card and get random results. A = ALL CAPS, C = Regular cap,
    T = Title Case, S = nospaces.
    """
    bot.say(fill_black(trigger.group(2)))


@commands('wc')
@example('.wc Batman # the night')
def _handle_wc(bot, trigger):
    """Submit one or two white cards. Separate with a #"""
    whites = trigger.group(2).split(' # ')

    if len(whites) in (1, 2):
        card = random.choice(black)
        while card.count('_') != len(whites):
            card = random.choice(black)
        bot.say(fill_black(card, whites))
    else:
        bot.say("One or two white cards only, please.")


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
    if modifier is 'C':    # Capitalizes the first letter
        return whitecard[0].capitalize() + whitecard[1:]
    elif modifier is 'T':  # Capitalizes the First Letter of Each Word
        return titlecase(whitecard)
    elif modifier is 'A':  # CAPITALIZES ALL LETTERS OH MY GOD
        return whitecard.upper()
    elif modifier is 'S':  # lowercaseandspacelesswithoutpunctuation
        return re.sub("\W", "", whitecard).lower()
    else:
        return whitecard


def load_cards(*args):
    """Grab white and black cards from text files in their respective directories."""
    global white, black
    white, black = (), ()
    # Get paths to card folders
    blackdir = os.path.join(os.path.dirname(__file__), 'blackcards')
    whitedir = os.path.join(os.path.dirname(__file__), 'whitecards')
    # Add each file's contents to the card list tuples. Files should be utf8 .txt files.
    for file in os.listdir(blackdir):
        if file.endswith('.txt'):
            with open(os.path.join(blackdir, file), 'r', encoding='utf-8') as f:
                black += tuple(x for x in f.read().splitlines() if not x.startswith('#'))
    for file in os.listdir(whitedir):
        if file.endswith('.txt'):
            with open(os.path.join(whitedir, file), 'r', encoding='utf-8') as f:
                white += tuple(x for x in f.read().splitlines() if not x.startswith('#'))

load_cards()
