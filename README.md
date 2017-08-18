# Fedt
Food Expiration Date Tracker. A command line Python tool to keep an eye on your food.

## About
Fedt is a command line only tool providing an interface to a user-defined list of food items and their expiration date. All items are saved in a plain text file, named ".food.dat" by default (can be changed at line 135 of fedt.py).

Current version: 0.9.5

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
display                            -> Show all registered items.
add [FOOD] [ISO_DATE] ([QUANTITY]) -> Add one [FOOD] item at [ISO_DATE] (YYYY-MM-DD) or more if optional [QUANTITY] is provided.
delete [FOOD] ([QUANTITY])         -> Remove one [FOOD] item or more if optional [QUANTITY] is provided.
update ([FILE_NAME])               -> Export the current list into default save file unless [FILE_NAME] is provided (does not update default file in this case).
revert                             -> Revert to the last default file update state, losing all unsaved changes.
exit/quit                          -> Quit the program.
help                               -> Show this message.
version                            -> Show current version and disclaimer.
```
