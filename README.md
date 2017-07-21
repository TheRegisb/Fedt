# Fedt
Food Expiration Date Tracker. A command line Python tool to keep an eye on your food.

## About
Fedt is a command line only tool providing an interface to a user-defined list of food items and their expiration date. All items are saved in a plain text file, named ".food.dat" by default (can be changed at line 119 of fedt.py).

Current version: 0.7

This program is distributed under GNU GPLv3+ license and you are free to run, study, modify and redistribute the code under certain conditions.

## Prerequisite
Fedt use plain Python 3. Make sure you have a 3.* version on your computer by typing `python3` in a terminal.
If not, update your system before installing the python3 package:
`sudo apt-get update && sudo apt-get upgrade && sudo apt-get install python3`

or for Arch-related systems:
`pacman -Syu && pacman -S python3`

## Usage
To use Fedt, either call the Python 3 interpreter:
`python3 ./fedt.py`
Or grant yourself the right to directly call it:
`chmod 755 ./fedt.py`
`./fedt.py`

You can now start Fedt and interact with the program. No command line arguments is currently supported.

8 commands are available:
```
display				-> Display all registered items, sorted by ascending expiration date
add [FOOD] [ISO_DATE]	   	-> Add [FOOD] item with [ISO_DATE] (YYYY-MM-DD) to the list
delete [FOOD]			-> Remove [FOOD] item from list
update (optional[FILE_NAME])	-> Export the current list to default save file, unless [FILE_NAME] is provided
revert 				-> Revert to the last update, discarding all unsaved changes
exit/quit			-> Leave the program; ask for confirmation if changes are pending
help				-> Display the list of all available command
version				-> Show current version and disclaimer
```
