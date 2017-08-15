#!/usr/bin/python3
#coding: utf-8
#
#  Fedt -- Food Expiration Date Tracker
#  Copyright (C) 2017 Régis BERTHELOT
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from os.path import isfile
from sys import exit, stderr
from operator import itemgetter
import datetime

class food_registry:
    food_dic = {} # Dictionary to be live edited, each member being NAME: [DATE, QUANTITY]
    bk_dic = {} # Backup, changed only upon self.export_current()
    filename = "" # Defined by user upon creation
    update = False # Keep track of unsaved changes

    # Look up for "filename" (./.food.dat by defaults)
    # Each line is formatted as NAME:ISO_DATE
    # Validate and add each line into food_dic

    def __init__(self, filename):
        self.filename = filename
        if (isfile(filename)):
            raw_file = open(filename, "r")
            lines = raw_file.readlines()
            lines = [x.strip('\n') for x in lines] # Lambda removing all carriage return

            for i in range(0, len(lines)):
                element = lines[i].split(':');
                if (len(element[0]) == 0):
                    raise ValueError("Error at line %d: No name registred." % (i + 1))
                if not (self.is_iso_date(element[1])):
                    raise ValueError("Error at line %d: Date is not ISO formated (YYYY-MM-DD)." % (i + 1))
                if (not element[2] or (element[2] and int(element[2]) <= 0)): # TODO test if element[2] is indeed an int
                    raise ValueError("Error at line %d: Quantity is missing or equal or lesser than 0." % (i + 1))
                self.food_dic[element[0]] = [element[1], int(element[2])]

            raw_file.close()
            self.bk_dic.update(self.food_dic)

    def is_iso_date(self, usr_date):
        try:
            datetime.datetime.strptime(usr_date, "%Y-%m-%d") # Check if string follow the ISO format YYYY-MM-DD
        except ValueError:
            return (False)
        return (True)

    def display(self):
        if (len(self.food_dic) == 0):
            print ("No registered item.")
        else:
            max_value = len(max(self.food_dic, key=len)) # Dynamically adapt the length for clean formatting
            sorted_food = sorted(self.food_dic.items(), key=itemgetter(1))
            for i in range(0, len(sorted_food)):
                print (sorted_food[i])
                # print ("%s %s: %s" % (sorted_food[i][0].ljust(max_value), "(xTODO quantity)", sorted_food[i][1][0].rjust(10))) # TODO quantity

    def add_food(self, name, date, quantity = 1):
        if not (self.is_iso_date(date)):
            print ("add: Date error (expected ISO date \"YYYY-MM-DD\").", file=stderr)
            return
        tmp_name = name.capitalize()
        i = 1
        while (tmp_name in self.food_dic): # If "name" is already inside, add a number at the end of the new one
            if (date == self.food_dic[tmp_name][0]): # Simply increase quantity if item share same name and date of exisiting item
                self.food_dic[tmp_name][1] += quantity
                break;
            tmp_name = name.capitalize() + "." + str(i) # Append a number in case of same name but different date
            i += 1
        else: # If item does not already exist, create a new entry
            tmp_item = [date, quantity]
            self.food_dic[tmp_name] = tmp_item
        self.update = True

    def delete_food(self, name):
        if (name in self.food_dic):
            self.food_dic.pop(name, None) # TODO rename duplicate
            self.update = True
        else:
            print ("remove: No \"%s\" item registered." % (name), file=stderr)

    def revert(self):
        if (update):
            command = str(input("All unsaved changes will be lost. Continue? [Yes/No]: ")).strip().lower()
            while (True):
                if (command == "y" or command == "yes"):
                    break ;
                elif (command == "n" or command == "no"):
                    return
                else:
                    command = str(input("Please answear [Yes/No]: ")).strip().lower()
        self.food_dic.clear()
        self.food_dic.update(self.bk_dic)
        print ("Current list reverted to last update.")
        self.update = False

    def export_current(self, path = None): # if no arguments provided, use default filename
        if (path == None):
            path = self.filename
        raw_file = open(path, "w")
        for item in self.food_dic:
            raw_file.write(item + ':' + self.food_dic[item][0] + ':' + str(self.food_dic[item][1]) + '\n')
        print ("Food list successfully exported to \"%s\" file." % (path))
        self.bk_dic.clear()
        self.bk_dic.update(self.food_dic)
        if (path == self.filename): # The update is no longer considered pending if default file is updated
            self.update = False

    def update_pending(self):
        return (self.update)


def main():
    current_register = food_registry(".food.dat") # Default save file name. Can be changed here before loading the program.

    while (True): # Interactive command menu
        command = str(input("Command: "))
        args = command.strip().lower().split(' ')

        if (args[0] == "display"):
            if (len(args) == 1):
                current_register.display()
            else:
                args_error(args[0])

        elif (args[0] == "add"):
            if (len(args) == 3):
                current_register.add_food(args[1].strip(), args[2])
            else:
                print ("add: Syntax error (expected \"add [FOOD_NAME] [ISO_DATE]\").", file=stderr)

        elif (args[0] == "delete"):
            if (len(args) == 2):
                current_register.delete_food(args[1].capitalize())
            else:
                print ("delete: Syntax error (expected \"delete [FOOD_NAME]\").", file=stderr)

        elif (args[0] == "update"):
            if (len(args) == 1 or len(args) == 2):
                current_register.export_current(None if len(args) == 1 else args[1])
            else:
                args_error(args[0])

        elif (args[0] == "revert"):
            if (len(args) == 1):
                current_register.revert()
            else:
                args_error(args[0])

        elif (args[0] == "help"):
            if (len(args) == 1):
                help_msg()
            else:
                args_error(args[0])

        elif (args[0] == "version"):
            if (len(args) == 1):
                version()
            else:
                args_error(args[0])

        elif (args[0] == "exit" or args[0] == "quit"):
            if (len(args) == 1):
                ask_leaving(current_register)
            else:
                args_error(args[0])

        elif (len(args[0]) == 0):
            continue

        else:
            print ("Error: Unknow command (type help for commands list).", file=stderr)

# Below are the function not relevant for the food_registry class itself

def args_error(cmd_name): # Common error message for one argument commands
    print ("%s: Too many arguments." % (cmd_name), file=stderr)

def help_msg():
    print ("display\t\t\t\tShow all registered items.\n"
           "add [food] [ISO_date]\t\tAdd the [food] item in list with the [ISO_date] (YYYY-MM-DD).\n"
           "delete [food]\t\t\tRemove said [food] if in list.\n"
           "update (optional[FILE_NAME])\tExport the current food list into default save file unless FILE_NAME is provided.\n"
           "revert\t\t\t\tRevert to the last update, losing all unsaved changes.\n"
           "exit/quit\t\t\tQuit the program.\n"
           "help\t\t\t\tShow this message."
           "version\t\tShow current version and disclaimer")

def version():
    print ("Fedt -- Food Expiration Date Tracker\n  Version: 0.7.2")
    print ("  Made by: Régis Berthelot")
    print ("  License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licences/gpl.htlm>")
    print ("  This software is free, and you are welcome to redistribute it under certain contitions.")
    print ("  This program comes with ABSOLUTELY NO WARRANTY");

def ask_leaving(cur_reg):
    if (cur_reg.update_pending()):
        command = str(input("Unsaved changes. Quit anyways? [Save/Yes/No]: ")).strip().lower()
        while (True):
            if (command == "s" or command == "save"):
                cur_reg.export_current()
                exit(0)
            elif (command == "y" or command == "yes"):
                exit(0)
            elif (command == "n" or command == "no"):
                break;
            command = str(input("Please answear [Save/Yes/No]: ")).strip().lower()
    else:
        exit(0)

if __name__ == "__main__":
    main()
