## Synopsis

"cah" and "humanity" are modules for the [Sopel IRC bot](https://sopel.chat/) meant to emulate the popular card game Cards Against Humanity. The "cah" module commands return random combinations of cards from games like Cards Against Humanity. The "humanity" module goes further and allows you to actually play the game with friends in your IRC chat room, dealing cards to each player for them to choose from.

## Installation

If you are already using the [Sopel IRC bot](https://sopel.chat/), installation is simple: put the included files in your Modules directory and rename the card files such as "cah-black-cards_example.txt" to "cah-black-cards.txt". The next time you load your bot, these files will be included and should be ready to go. For "humanity", you will also want to edit the line near the top of the file to select a room for it to be played in.


## cah Commands

**.hate**: The main command to return a random combination of black and white cards. If you're lucky, it will even be funny.

**.bc**: Provide your own black card to be filled with random white cards, using underscores for the blanks. Example: ___.bc I used to like \_ until I discovered \_.___ Note: cah-black-cards_example.txt has information on additional blank formatting tricks to return cards with capitalization or titlecase.

**.wc**: Provide your own white card or cards to be plugged into a random black card. Additional cards are separated by a #. Example: ___.wc your mom___ Example 2: ___.wc your mom # your cat___.

**.cardcount**: Return the number of black and white cards.

**.cahload**: Reload the cards from the .txt files and return the number of black and white cards.


## humanity Commands

**.cah**: Starts the game. You can append a number to the end to set the points required for victory. Example: ___.cah 5___

**.cahjoin**: Join a game in progress.

**.cahstart**: The creator can start the game once everyone has joined.

**.rando**: Adds Rando Cardrissian to the game. He plays random cards each turn. Sometimes he even wins. Be embarrassed if this happens.

**.cahplay** or **.cp**: Play a card. Example: ___.cp 2___ or ___.cahplay 4 5___ for a two-blank card.

**.cahvote** or **.cv**: Vote for a card if you are the czar. Example: ___.cv 2___

**.cahscores**: Get the current scores.

**.cahleave**: Leave a game in progress. This needs testing as it may break things.

**.cahstop**: The creator can stop a game in progress. Currently, this is the only way to stop the game other than an admin ___.reload___ of the module.


## Customization

If you don't like the default command triggers, they can be edited in the .py files. More importantly, you can edit the card .txt files to include whatever cards you want. The line "self.winning_score = 3" in "humanity.py" can also be altered to change the default victory score.

## Credits

These modules were created by Morbiac and Winter. "CAH" cards are taken from Cards Against Humanity under a Creative Commons BY-NC-SA 2.0 license. https://cardsagainsthumanity.com/

This application is not endorsed by Cards Against Humanity.

Carps & Angsty Manatee cards are from http://carpsandangstymanatee.com under a Creative Commons BY-NC-SA 2.0 license