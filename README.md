# RPG Tactical Fantasy Game

__WARNING__ : GRIMMY/Original Author: "This game is entirely under construction."

The game is an RPG Tactical Fantasy game, turn-based and is in 2D.
I'm currently looking for a good name.

## How to start the game

If you are using 64-bit Windows you can head over to the [releases page](https://github.com/grimmys/rpg_tactical_fantasy_game/releases) to get a prebuilt executable.

If you would rather run directly from the source \(or want to develop the game\), make sure to have [Python](https://python.org) installed and run `python -m pip install -r requirements.txt` in the repository folder.

DISCLAIMER: Damian Domela: "Sounds were disabled and images were converted to .bmp to increase the project its adaptability towards different versions of PyGame/OS.
The current version of PyGame mentioned in requirements.txt is what worked for my MacBook Air, if you're having trouble with installation, try adapting the PyGame version to what better suits your OS."

Then you can run `python3 main.py` to start the game.

## Keys

* Left click : Select a player, choose a case to move, select an action to do etc (main button)
* Left click (on any empty tile) : Open main menu
* Left click (on any entity that is not a player who has finished his turn) : Open a window giving information about the entity
* Right click : Deselect a player or cancel last action if possible (secondary button)
* Right click (on any entity) : Show the possible movements of the entity
