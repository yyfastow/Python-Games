import copy
import os
import sys


def clear():
    """ Clears the screen """
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def boards():
    """ makes a dict with values from 1a to 3c for tictacttoe board """
    board = {}
    for num in range(1,4):
        for letter in 'abc':
            box = "{}{}".format(num, letter)
            board[box] = ' '
    return board


def draw_board(board):
    """ draws board """
    print(" |a|b|c|")
    for num in range(1,4):
        print("{}|".format(num), end='')
        for letter in "abc":
            box = "{}{}".format(num, letter)
            print("{}|".format(board[box]), end='')
        print("")


def turn(board, player):
    """ goes through turn letting player move a piece """
    print("\n\nPlayer '{}' turn:\n".format(player))
    while True:
        move = input("Where do you want to move:  ")
        try:
            if board[move] == ' ':
                board[move] = player
                break
        except KeyError:
            pass
    if won(board, player):
        print("Yeah {} won!!!!\n\n".format(player))
        replay = input("Do you want to replay:   ")
        if replay.lower() == 'yes':
            game()
        else:
            print("Thanks for playing!\nExiting....")
            sys.exit(0)
        


def won(board, player):
    """checks if player won """
    box = ""
    for num in range(1,4):
        for letter in 'abc':
            box = "{}{}".format(num, letter)
            if board[box] != player:
                break
        else:
            return True
    for letter in 'abc':
        for num in range(1,4):
            box= "{}{}".format(num,letter)
            if board[box] != player:
            break
        else:
            return True
    if board['1a'] == player and board['2b'] == player and board['3c'] == player:
        return True
    elif board['3a'] == player and board['2b'] == player and board['1c'] == player:
        return True
    return False
        

        

def game():
    """ plays game """
    board = boards()
    while True:
        draw_board(board)
        turn(board, "X")
        draw_board(board)
        turn(board, "O")


game()
