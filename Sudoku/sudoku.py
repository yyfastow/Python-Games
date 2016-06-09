import copy
import json
import os
import random
import sys

from sudoku_sheets import sudoku_list



def clear():
    """ Clears the screen """
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def draw_board(sudoku_board):
    """ prints the sudoku board """
    print("  1 2 3|4 5 6|7 8 9|")
    # print("*" * 21)
    box = ""
    for letter in "ABCDEFGHI":
        print("{}|".format(letter), end='')
        for num in range(1,10):
            box = "{}{}".format(letter, num)
            for key, dicty in enumerate(sudoku_board):
                if box in dicty:
                    if sudoku_board[key][box] == 0:
                        print(" |", end='')
                    else:
                        print("{}|".format(sudoku_board[key][box]), end='')
                    break
        print("")
    print("*" * 21)

def add(sudoku_board, sudoku_sheet, num, key, box, action):
    """ Adds or changes number from given box """
    saved_game = open('saved_games.json', 'w')
    sudoku_board[key][box] = int(num)
    print("{} {} in {} place".format(action, num, box))
    json.dump(sudoku_board, saved_game, sort_keys=True)
    saved_game.closed
    saved_game = open('saved_games.json', 'r')
    sudoku_json = json.load(saved_game)
    game(sudoku_json, sudoku_sheet)
    saved_game.closed
    print("Game was saved")


def delete(sudoku_board, sudoku_sheet, key, box):
    """ Deletes given box """
    saved_game = open('saved_games.json', 'w')
    print("deleted {} in {}.".format(sudoku_board[key][box], box))
    sudoku_board[key][box] = 0
    json.dump(sudoku_board, saved_game, sort_keys=True)
    saved_game.closed
    saved_game = open('saved_games.json', 'r')
    sudoku_json = json.load(saved_game)
    game(sudoku_json, sudoku_sheet)
    saved_game.closed
    

def won(sudoku_board):
    """ checks if you won and ends game """
    for index, dicty in enumerate(sudoku_board):
        for key, value in dicty.items():
            if value == 0:
                return False
    if check_all(sudoku_board) == True:
        print("You Won!!!!!!!!!!")
        open_file()
        system.exit(0)
            

def checker(key, value, check_list):
    """does the real checking of the details given by check_all """
    mistake = False
    for check_key, check_value in check_list.items():
        if value == check_value:
            print("Box {} and {} are the same number: {}".format(
                    key, check_key, value))
            mistake = True
    if value != 0:
        check_list[key] = value
    return mistake


def check_all(sudoku_board):
    """ Checks if there any mistakes in sudoku game """
    # could use it every turn or only when user demands it
    # or only tell if problem and not what problem is
    mistake = False
    for index, dicty in enumerate(sudoku_board):
        check_list = {}
        for key, value in dicty.items():
            if checker(key, value, check_list) == True:
                mistake = True
                    
    for letter in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']:
        check_list = {}
        for number in range(1, 10):
            box = "{}{}".format(letter, number)
            for key in range(0,9):
                if box in sudoku_board[key]:
                    if checker(box, sudoku_board[key][box], check_list) == True:
                        mistake = True

    for number in range(1, 10):
        check_list = {}
        for letter in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']:
            box = "{}{}".format(letter, number)
            for key in range(0,9):
                if box in sudoku_board[key]:
                    if checker(box, sudoku_board[key][box], check_list) == True:
                        mistake = True
    if mistake == False:
        print("No mistakes everything is in order! \n\n")
        return True


 


def validator(box, sudoku_board, original, command, num=0):
    """ validates if you could change, delete or add at given box"""
    action = 'Adding'
    sudoku_box = ""
    for key, dicty in enumerate(sudoku_board):
        if box in dicty:
            sudoku_box = sudoku_board[key][box]
            if original[key][box] == 0 and sudoku_board[key][box] != 0:
                if command == 'add':
                    action = 'Changing {} to'.format(sudoku_box)
                    add(sudoku_board, num, original, key, box, action)
                elif command == 'delete':
                    delete(sudoku_board, original, key, box)
            elif original[key][box] != 0:
                print("You can't delete or change numbers from the original")
                turn(sudoku_board, original)
            elif sudoku_board[key][box] == 0:
                if command == 'add':
                    add(sudoku_board, original, num, key, box, action)
                else:
                    print("Allready empty no need to delete")
                    turn(sudoku_board, original)
            break
    else:
        print("Make sure to put proper spot number like A4.")
        turn(sudoku_board, original)


def rules():
    """ prints rules of sudoku game."""
    print("""The rules of sudoku are simple: each of the nine blocks has to
        contain all the numbers 1-9 within its squares.
        Each number can only appear once in a row, column or box.

You can not delete any numbers that are not in the original sudoku,
        or to the list the game arginialy started with.

Good Luck!
          """)


def turn(sudoku_board, original):
    """allows player to add or delete number and get help or quit."""
    command = input("What command do you want to do (add/delete/quit/help/check/save/open):  ")
    num = 0
    if command.lower() == 'add':
        try:
            num = int(input("Which number do you want to add:  "))
        except ValueError:
            pass
        if num not in range(1,10):
            print("number must be between 1 to 9. Try again!")
            turn(sudoku_board, original)
        else:
            box = input("And in which spot (answer like A2 or D8):   ").upper()
            validator(box, sudoku_board, original, command, num)
    elif command.lower() == 'delete':
        print("Make sure to look at original.You cant delete any number from orginal.")
        box = input("Which spot do you want to delete (answer like A2):  ").upper()
        validator(box, sudoku_board, original, command)
    elif command.lower() == 'quit':
        sure = input("Are you sure:  ")
        if sure.lower() == 'yes':
            print("turning off!!")
            sys.exit(0)
        else:
            turn(sudoku_board, original)
    elif command.lower() == "help":
        rules()
        print("to learn more look up this url:")
        print("     http://www.conceptispuzzles.com/?uri=puzzle/sudoku/rules")
        print("\n\n")
        turn(sudoku_board, original)
    elif command.lower() == 'check':
        print("\n")
        check_all(sudoku_board)
    elif command.lower() == 'save':
        saved_game = open('saved_games.json', 'w')
        json.dump(sudoku_board, saved_game, sort_keys=True)
        saved_game.closed
        print("Game was saved")
    elif command.lower() == 'open':
        saved_game = open('saved_games.json', 'r')
        sudoku_json = json.load(saved_game)
        game(sudoku_json)
        saved_game.closed

        print("on saved file!")
    else:
        print("Try again")
        turn(sudoku_board, original)


def open_file():
    """ starts the game by opening saved file or restarting """
    option = input("restart/new:  ")
    sure = 'no'
    sudoku_sheet = {}
    if option.lower() == 'new':
        sudoku_sheet = random.choice(sudoku_list)
        saved_type = open('type_sudoku.json', 'w')
        json.dump(sudoku_sheet, saved_type, sort_keys=True)
        saved_type.close
    else:
        saved_sheet = open('type_sudoku.json', 'r')
        sudoku_sheet = json.load(saved_sheet)
        saved_sheet.close
    if option.lower() != 'restart' and option.lower() != 'new':
        saved_game = open('saved_games.json', 'r')
        sudoku_json = json.load(saved_game)
        saved_game.closed
        game(sudoku_json, sudoku_sheet)
    else:
        sudoku_board = copy.deepcopy(sudoku_sheet)
        new_game(sudoku_board, sudoku_sheet)


def new_game(sudoku_board, sudoku_sheet):
    """ the loop of a new game"""
    clear()
    print("welcome to sudoku!")
    rules()
    while True:
        print("\n\n")
        print("Game now:")
        draw_board(sudoku_board)
        turn(sudoku_board, sudoku_sheet)
        print("\n\n")
        print("Original:")
        draw_board(sudoku_sheet)


def game(sudoku_board, sudoku_sheet):
    clear()
    print("welcome to sudoku!")
    rules()
    while True:
        print("\n\n")
        print("Original:")
        draw_board(sudoku_sheet)
        print("\n\n")
        print("Game now:")
        draw_board(sudoku_board)
        turn(sudoku_board, sudoku_sheet)


open_file()
                
