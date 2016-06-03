import copy
import json
import os
import sys


sudoku_sheet = [{"A1":7, "A2":0, "A3":1, "B1":4, "B2": 6, "B3":0,
                 "C1":0, "C2":8, "C3":0}, {"A4":0, "A5": 5, "A6":8,
                 "B4":1, "B5":7, "B6":0, "C4":0, "C5": 4, "C6":0},
                 {"A7":9, "A8":2, "A9":0, "B7":8, "B8": 0, "B9":0,
                 "C7":0, "C8":6, "C9":0},
                {"D1":0, "D2": 0, "D3":9,"E1":0, "E2":0, "E3":6,
                 "F1":0, "F2": 0, "F3":4}, {"D4":0, "D5": 0, "D6":0,
                 "E4":4, "E5":0, "E6":7, "F4":0, "F5": 0, "F6":0},
                 {"D7":1, "D8":0, "D9":0, "E7":2, "E8": 0, "E9":0,
                 "F7":5, "F8":0, "F9":0},
                {"G1":0, "G2":9, "G3":0, "H1":0, "H2": 0, "H3":3,
                 "I1":0, "I2":4, "I3":7}, {"G4":0, "G5": 6, "G6":0,
                 "H4":0, "H5":8, "H6":1, "I4":9, "I5": 2, "I6":0},
                 {"G7":0, "G8":1, "G9":0, "H7":0, "H8": 9, "H9":2,
                 "I7":6, "I8":0, "I9":8}]


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

def add(sudoku_board, num, key, box, action):
    """ Adds or changes number from given box """
    saved_game = open('saved_games.json', 'w')
    sudoku_board[key][box] = int(num)
    print("{} {} in {} place".format(action, num, box))
    json.dump(sudoku_board, saved_game, sort_keys=True)
    saved_game.closed
    saved_game = open('saved_games.json', 'r')
    sudoku_json = json.load(saved_game)
    game(sudoku_json)
    saved_game.closed
    print("Game was saved")


def delete(sudoku_board, key, box):
    """ Deletes given box """
    saved_game = open('saved_games.json', 'w')
    print("deleted {} in {}.".format(sudoku_board[key][box], box))
    sudoku_board[key][box] = 0
    json.dump(sudoku_board, saved_game, sort_keys=True)
    saved_game.closed
    saved_game = open('saved_games.json', 'r')
    sudoku_json = json.load(saved_game)
    game(sudoku_json)
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
                    add(sudoku_board, num, key, box, action)
                elif command == 'delete':
                    delete(sudoku_board, key, box)
            elif original[key][box] != 0:
                print("You can't delete or change numbers from the original")
                turn(sudoku_board, original)
            elif sudoku_board[key][box] == 0:
                if command == 'add':
                    add(sudoku_board, num, key, box, action)
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
    new_game = input("New Game:  ")
    sure = 'no'
    if new_game.lower() == 'yes':
        sure = input("are you sure (old data will be lost):  ")
    if sure.lower() == 'yes':
        sudoku_board = copy.deepcopy(sudoku_sheet)
        new_game(sudoku_board)
    else:
        saved_game = open('saved_games.json', 'r')
        sudoku_json = json.load(saved_game)
        game(sudoku_json)
        saved_game.closed


def new_game(sudoku_board):
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


def game(sudoku_board):
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
                
