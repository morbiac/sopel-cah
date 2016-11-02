## Synopsis

"cah" and "humanity" are modules for the [Sopel IRC bot](https://sopel.chat/) meant to emulate the popular card game Cards Against Humanity. The "cah" module commands return random combinations of cards from games like Cards Against Humanity. The "humanity" module goes further and allows you to actually play the game with friends in your IRC chat room, dealing cards to each player for them to choose from.

## Installation

If you are already using the [Sopel IRC bot](https://sopel.chat/), installation is simple: put the included files (and card directories) in your Modules directory. The next time you load your bot, these files will be included and should be ready to go. For "humanity", you will also want to edit the line near the top of the file to select an IRC channel for it to be played in.


## cah Commands

`.hate`: The main command to return a random combination of black and white cards. If you're lucky, it will even be funny.

`.bc`: Provide your own black card to be filled with random white cards, using underscores for the blanks. Example: `.bc I used to like \_ until I discovered \_`. Note: `cah_black.txt` has information on additional blank formatting tricks to return cards with capitalization or titlecase.

`.wc`: Provide your own white card or cards to be plugged into a random black card. Additional cards are separated by a #. Example: `.wc your mom` Example 2: `.wc your mom # your cat`.

`.cardcount`: Return the number of black and white cards.

`.cahload`: Reload the cards from the .txt files and return the number of black and white cards.


## humanity Commands

`.cah`: Starts the game. You can append a number to the end to set the points required for victory. Example: `.cah 5`

`.cahjoin`: Join a game in progress.

`.cahstart`: The creator can start the game once everyone has joined.

`.rando`: Adds Rando Cardrissian to the game. He plays random cards each turn. Sometimes he even wins. Be embarrassed if this happens.

`.cahplay` or `.cp`: Play a card. Example: `.cp 2` or `.cahplay 4 5` for a two-blank card.

`.cahvote` or `.cv`: Vote for a card if you are the czar. Example: `.cv 2`

`.cahscores`: Get the current scores.

`.cahleave`: Leave a game in progress. This needs testing as it may break things.

`.cahrepeat` or `.cr`: Repeat the current black card for the round.

`.cahstop`: The creator can stop a game in progress. Currently, this is the only way to stop the game other than an admin `.reload` of the module.


## Customization

If you don't like the default command triggers, or if they overlap with existing commands, they can be edited in the .py files. More importantly, you can edit the card .txt files or create your own to include whatever cards you want. The line `self.winning_score = 3` in "humanity.py" can also be altered to change the default victory score.

Note: .txt files may need to be saved in utf-8 format rather than, for example, ANSI. This needs more testing.

## Credits

These modules were created by Morbiac and Winter.

"CAH" cards are taken from Cards Against Humanity under a Creative Commons BY-NC-SA 2.0 license. https://cardsagainsthumanity.com/

This application is not endorsed by Cards Against Humanity.

Carps & Angsty Manatee cards are from http://carpsandangstymanatee.com under a Creative Commons BY-NC-SA 2.0 license